#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
運輸需求矩陣解析與動態匯入模組 (Demand Importer)
=============================================================================
支援格式：標準 Excel (.xlsx / .xls) 矩陣，例如 Demand_from_to.xlsx
功能：
  1. 解析 7 大廠區 (FAB8AB, FAB8CD, FAB8E, FAB8F, FAB8S, 嘉晶篤行, 嘉晶創新) 需求矩陣。
  2. 自動校正廠區名稱別名與空白、換行。
  3. 驗證資料有效性（非負整數、對角線為0、總需求合理性）。
  4. 寫入 logistics.db 之 demand_matrix 表。
=============================================================================
"""

import sys
import io
import math
import sqlite3
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# 7 大標準廠區代碼
STANDARD_FABS = [
    'FAB8AB',
    'FAB8CD',
    'FAB8E',
    'FAB8F',
    'FAB8S',
    '嘉晶篤行',
    '嘉晶創新'
]

# 廠區別名對照表
FAB_ALIAS_MAP = {
    'FAB8AB': 'FAB8AB',
    '8AB': 'FAB8AB',
    '8AB 廠': 'FAB8AB',
    '8AB 廠大廳': 'FAB8AB',
    'FAB8CD': 'FAB8CD',
    '8CD': 'FAB8CD',
    '8CD 廠': 'FAB8CD',
    '8CD 廠碼頭': 'FAB8CD',
    'FAB8E': 'FAB8E',
    '8E': 'FAB8E',
    '8E 廠': 'FAB8E',
    '8E 廠大廳': 'FAB8E',
    'FAB8F': 'FAB8F',
    '8F': 'FAB8F',
    '8F 廠': 'FAB8F',
    '8F 廠代工碼頭': 'FAB8F',
    'FAB8S': 'FAB8S',
    '8S': 'FAB8S',
    '8S 廠': 'FAB8S',
    '8S 廠大廳': 'FAB8S',
    '嘉晶 (篤行)': '嘉晶篤行',
    '嘉晶(篤行)': '嘉晶篤行',
    '嘉晶 篤行': '嘉晶篤行',
    '嘉晶篤行': '嘉晶篤行',
    '篤行': '嘉晶篤行',
    '嘉晶 (創新)': '嘉晶創新',
    '嘉晶(創新)': '嘉晶創新',
    '嘉晶 創新': '嘉晶創新',
    '嘉晶創新': '嘉晶創新',
    '創新': '嘉晶創新',
}


def normalize_fab_name(name_str):
    if not isinstance(name_str, str):
        return None
    cleaned = name_str.strip().replace('\r', '').replace('\n', '')
    if cleaned in FAB_ALIAS_MAP:
        return FAB_ALIAS_MAP[cleaned]
    # Check normalized substring
    for alias, std in FAB_ALIAS_MAP.items():
        if alias.lower() == cleaned.lower():
            return std
    return None


def parse_demand_excel(file_source):
    """
    解析 Excel 檔案（可為檔案路徑、bytes、或 io.BytesIO 物件）。
    回傳字典：
      {
        'matrix': { (from_fab, to_fab): int_batches },
        'total_demand_24h': int,
        'active_corridors_count': int,
        'grid_data': { 'fabs': [...], 'values': { from: { to: batches } }, 'row_sums': {}, 'col_sums': {} }
      }
    """
    if isinstance(file_source, bytes):
        file_source = io.BytesIO(file_source)

    # 讀取 Excel（不設 header 以便搜尋定位）
    raw_df = pd.read_excel(file_source, header=None)

    # 搜尋表頭列（包含 FAB8AB、FAB8CD 等廠區之列）
    header_row_idx = None
    col_mapping = {}  # col_idx -> standard_fab

    for r_idx in range(min(15, len(raw_df))):
        row_vals = raw_df.iloc[r_idx].tolist()
        matched = {}
        for c_idx, val in enumerate(row_vals):
            if pd.notna(val):
                std_fab = normalize_fab_name(str(val))
                if std_fab:
                    matched[c_idx] = std_fab
        # 若該列包含至少 3 個標準廠區，視為目標表頭
        if len(matched) >= 3:
            header_row_idx = r_idx
            col_mapping = matched
            break

    if header_row_idx is None:
        raise ValueError("未能自上傳的 Excel 中辨識出 7 大廠區欄位標題，請確認使用正確範本！")

    # 搜尋出發廠區（From）列
    row_mapping = {}  # row_idx -> standard_fab
    for r_idx in range(header_row_idx + 1, len(raw_df)):
        # 尋找前 3 個欄位中是否有廠區名稱
        for c_idx in range(min(4, raw_df.shape[1])):
            val = raw_df.iloc[r_idx, c_idx]
            if pd.notna(val):
                std_fab = normalize_fab_name(str(val))
                if std_fab and std_fab not in row_mapping.values():
                    row_mapping[r_idx] = std_fab
                    break

    if len(row_mapping) < 3:
        raise ValueError("未能自上傳的 Excel 中辨識出足夠的出發廠區 (From)，請確認範本格式！")

    matrix = {}
    grid_values = {f: {t: 0 for t in STANDARD_FABS} for f in STANDARD_FABS}
    row_sums = {f: 0 for f in STANDARD_FABS}
    col_sums = {t: 0 for t in STANDARD_FABS}

    for r_idx, from_fab in row_mapping.items():
        for c_idx, to_fab in col_mapping.items():
            if from_fab == to_fab:
                continue
            val = raw_df.iloc[r_idx, c_idx]
            batches = 0
            if pd.notna(val):
                try:
                    batches = int(round(float(val)))
                except (ValueError, TypeError):
                    batches = 0
            if batches < 0:
                raise ValueError(f"走廊 [{from_fab} ➔ {to_fab}] 之需求量不可為負數 ({batches})！")
            
            grid_values[from_fab][to_fab] = batches
            row_sums[from_fab] += batches
            col_sums[to_fab] += batches
            if batches > 0:
                matrix[(from_fab, to_fab)] = batches

    total_demand_24h = sum(matrix.values())
    if total_demand_24h <= 0:
        raise ValueError("上傳的需求矩陣總需求量為 0，請確認數值填寫！")

    corridors_list = []
    for (f, t), b in matrix.items():
        if b > 0:
            corridors_list.append({
                'from': f,
                'to': t,
                'batches': b,
                'demand_24h': b,
                'demand_shift': round(b / 2),
                'bidirectional_24h': b * 2
            })
    corridors_list.sort(key=lambda x: x['batches'], reverse=True)

    # Provide UI-compatible fabs array with parentheses
    ui_fabs = [
        'FAB8AB', 'FAB8CD', 'FAB8E', 'FAB8F', 'FAB8S',
        '嘉晶 (篤行)', '嘉晶 (創新)'
    ]
    ui_matrix = {}
    ui_row_sums = {}
    ui_col_sums = {}

    def to_ui_fab(name):
        if '篤行' in name: return '嘉晶 (篤行)'
        if '創新' in name: return '嘉晶 (創新)'
        return name

    for f in ui_fabs:
        ui_matrix[f] = {}
        ui_row_sums[f] = 0
        ui_col_sums[f] = 0

    for (f_raw, t_raw), b in matrix.items():
        fu = to_ui_fab(f_raw)
        tu = to_ui_fab(t_raw)
        if fu in ui_matrix and tu in ui_matrix[fu]:
            ui_matrix[fu][tu] = b
            ui_row_sums[fu] += b
            ui_col_sums[tu] += b

    return {
        'matrix': matrix,
        'total_demand_24h': total_demand_24h,
        'active_corridors_count': len(matrix),
        'grid_data': {
            'fabs': ui_fabs,
            'matrix': ui_matrix,
            'values': ui_matrix,
            'row_sums': ui_row_sums,
            'col_sums': ui_col_sums,
            'corridors': corridors_list,
            'total_sum': total_demand_24h,
            'total': total_demand_24h
        }
    }


def import_demand_to_db(matrix_dict, db_path='logistics.db'):
    """
    將解析後之 demand 矩陣寫入 SQLite 資料庫之 demand_matrix 表，
    並同步更新 fabs 資料表之出廠 (demand_out_24h)、進廠 (demand_in_24h) 與總需求 (demand_excel_sum)。
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 確保 table 存在
    c.execute("""
    CREATE TABLE IF NOT EXISTS demand_matrix (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_fab TEXT NOT NULL,
        to_fab TEXT NOT NULL,
        demand_batches INTEGER NOT NULL,
        demand_shift_batches INTEGER NOT NULL
    )
    """)

    # 清空現有需求矩陣
    c.execute("DELETE FROM demand_matrix")

    # 依需求量排序寫入
    sorted_pairs = sorted(matrix_dict.items(), key=lambda x: -x[1])
    fab_out = {f: 0 for f in STANDARD_FABS}
    fab_in = {f: 0 for f in STANDARD_FABS}

    for (from_fab, to_fab), dem24 in sorted_pairs:
        dem_shift = math.ceil(dem24 / 2.0)
        c.execute("""
        INSERT INTO demand_matrix (from_fab, to_fab, demand_batches, demand_shift_batches)
        VALUES (?, ?, ?, ?)
        """, (from_fab, to_fab, dem24, dem_shift))
        if from_fab in fab_out:
            fab_out[from_fab] += dem24
        if to_fab in fab_in:
            fab_in[to_fab] += dem24

    # 更新 fabs 表格之需求欄位
    for f in STANDARD_FABS:
        d_out = fab_out.get(f, 0)
        d_in = fab_in.get(f, 0)
        d_sum = max(d_out, d_in)
        c.execute("""
        UPDATE fabs
        SET demand_out_24h = ?, demand_in_24h = ?, demand_excel_sum = ?
        WHERE code = ?
        """, (d_out, d_in, d_sum, f))

    conn.commit()
    conn.close()
    return len(sorted_pairs)


if __name__ == '__main__':
    test_file = 'Demand_from_to.xlsx'
    print(f"測試讀取: {test_file}")
    res = parse_demand_excel(test_file)
    print(f"成功解析！總需求: {res['total_demand_24h']} 批, 活躍走廊數: {res['active_corridors_count']}")
    print("前 5 大需求走廊:")
    sorted_items = sorted(res['matrix'].items(), key=lambda x: -x[1])[:5]
    for (f, t), b in sorted_items:
        print(f"  {f} -> {t}: {b} 批")
