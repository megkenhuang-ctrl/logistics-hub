# -*- coding: utf-8 -*-
"""
半導體廠區物流排程 - 實際營運出勤與動態運能計算引擎 (Actual Operations Engine)
關聯司機每日班表 (driver_roster)，將出勤車輛（含 Car U）之動態運能與走廊需求即時比對，
精確計算當班/當日走廊利用率並標記 Overloading 斷料風險。
"""

import sqlite3
import re
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from validator import parse_od_pairs, norm_fab

DB_PATH = os.path.join(BASE_DIR, 'logistics.db')

def evaluate_actual_operations(db_path=DB_PATH, date_str='2026-11-01', shift='all', table_name='schedules_plan3'):
    """
    動態營運模式評估核心
    :param db_path: SQLite 資料庫路徑
    :param date_str: 營運日期 (YYYY-MM-DD)
    :param shift: 班別 ('all', 'day', 'night')
    :param table_name: 基準排程表 ('schedules_plan3', 'schedules_plan2', 'schedules')
    """
    if table_name not in ['schedules', 'schedules_plan2', 'schedules_plan3']:
        table_name = 'schedules_plan3'

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # 1. 查詢司機排班出勤狀態
    roster_query = "SELECT * FROM driver_roster WHERE date = ?"
    roster_args = [date_str]
    if shift in ['day', 'night']:
        roster_query += " AND lower(shift) = ?"
        roster_args.append(shift)

    roster_rows = conn.execute(roster_query, roster_args).fetchall()
    
    active_cars = set()
    car_roster_map = {}
    
    # 支援全日模式下的車輛統計
    for r in roster_rows:
        cid = r['car_id']
        # 全日模式下若某車在任一班次有執勤，則標註有出勤
        if cid not in car_roster_map:
            car_roster_map[cid] = {
                'car_id': cid,
                'car_name': r['car_name'],
                'driver': r['driver'],
                'plate': r['plate'] or '—',
                'status': r['status'],
                'shift': r['shift'],
                'shift_zh': r['shift_zh']
            }
        else:
            # 若全日模式且夜班執勤，更新司機資訊
            if r['status'] == '執勤':
                car_roster_map[cid]['status'] = '執勤'
                car_roster_map[cid]['driver'] = r['driver']
                if r['plate']:
                    car_roster_map[cid]['plate'] = r['plate']

        if r['status'] == '執勤':
            active_cars.add(cid)

    # 2. 查詢排程站點 (依據 active_cars 與 shift)
    sched_query = f"SELECT * FROM {table_name} WHERE 1=1"
    sched_args = []
    if shift in ['day', 'night']:
        sched_query += " AND shift = ?"
        sched_args.append(shift)

    sched_rows = conn.execute(sched_query, sched_args).fetchall()

    corridor_cap_total = {}
    corridor_cap_no_u = {}
    u_boost_batches = 0

    for row in sched_rows:
        cid = row['car_id']
        # 若是全日模式，需確認該班別該車是否在勤
        if shift == 'all':
            # 檢查特定 shift 該車是否在勤
            row_shift = row['shift'].lower()
            is_active_for_shift = any(
                r['car_id'] == cid and r['shift'].lower() == row_shift and r['status'] == '執勤'
                for r in roster_rows
            )
            if not is_active_for_shift:
                continue
        else:
            if cid not in active_cars:
                continue

        flows = parse_od_pairs(dict(row))
        for (orig, dest, batches) in flows:
            k = f"{orig} ➔ {dest}"
            corridor_cap_total[k] = corridor_cap_total.get(k, 0) + batches
            if cid == 'Car_U':
                u_boost_batches += batches
            else:
                corridor_cap_no_u[k] = corridor_cap_no_u.get(k, 0) + batches

    # 3. 查詢走廊基準需求
    demands = conn.execute("SELECT from_fab, to_fab, demand_batches FROM demand_matrix WHERE demand_batches > 0").fetchall()
    conn.close()

    corridor_results = []
    overloaded_count = 0
    tight_count = 0
    normal_count = 0
    total_demand = 0
    total_capacity = sum(corridor_cap_total.values())

    for d in demands:
        orig = norm_fab(d['from_fab'])
        dest = norm_fab(d['to_fab'])
        k = f"{orig} ➔ {dest}"
        
        daily_d = d['demand_batches']
        shift_d = daily_d if shift == 'all' else round(daily_d * 0.5)
        total_demand += shift_d

        cap = corridor_cap_total.get(k, 0)
        cap_no_u = corridor_cap_no_u.get(k, 0)
        u_contrib = cap - cap_no_u

        if cap > 0:
            util = round(shift_d / cap * 100, 1)
        else:
            util = 999.9 if shift_d > 0 else 0.0

        is_over = (util > 100.0) or (shift_d > 0 and cap == 0)
        is_tight = (not is_over) and (util > 85.0)

        if is_over:
            overloaded_count += 1
            status = 'OVERLOADED'
        elif is_tight:
            tight_count += 1
            status = 'TIGHT'
        else:
            normal_count += 1
            status = 'NORMAL'

        corridor_results.append({
            'corridor': k,
            'from_fab': d['from_fab'],
            'to_fab': d['to_fab'],
            'demand': shift_d,
            'capacity': cap,
            'u_contrib': u_contrib,
            'utilization': util,
            'is_overloaded': is_over,
            'shortfall': max(0, shift_d - cap),
            'status': status
        })

    corridor_results.sort(key=lambda x: x['utilization'], reverse=True)
    
    valid_utils = [c['utilization'] for c in corridor_results if c['utilization'] < 900]
    max_util = max(valid_utils) if valid_utils else 0.0
    avg_util = round(sum(valid_utils) / len(valid_utils), 1) if valid_utils else 0.0

    return {
        'status': 'success',
        'date': date_str,
        'shift': shift,
        'table': table_name,
        'active_cars': sorted(list(active_cars)),
        'total_active_cars': len(active_cars),
        'u_car_active': ('Car_U' in active_cars),
        'u_boost_batches': u_boost_batches,
        'car_roster': car_roster_map,
        'total_demand': total_demand,
        'total_capacity': total_capacity,
        'overloaded_count': overloaded_count,
        'tight_count': tight_count,
        'normal_count': normal_count,
        'max_utilization': max_util,
        'avg_utilization': avg_util,
        'corridors': corridor_results
    }
