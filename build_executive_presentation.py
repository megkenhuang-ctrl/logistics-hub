# -*- coding: utf-8 -*-
"""
=============================================================================
半導體廠區物流排程優化 - 高階主管報告與演算法規格 簡報生成器
=============================================================================
風格標準：參考「現況診斷與運籌痛點分析_可編輯簡報.pptx」
特點：
  1. 16:9 寬螢幕高階暗色科技風格 (Dark-Tech Boardroom Aesthetic, #070F1C)
  2. 100% 原生可編輯形狀、文字框與高對比色階 (深藍底、白字、青綠高亮、紅黃警示)
  3. 四大核心維度：
     - Slide 1: 高階主管報告摘要 (Executive Summary: 痛點診斷 vs. 方案三 100% 突破效益)
     - Slide 2: 系統規格與數學約束模型 (System Specifications & Math Formulation)
     - Slide 3: 兩階段解耦演算法架構 (Two-Stage Decoupling: MILP + CP-SAT)
     - Slide 4: AI 工具鏈端到端解題方法論 (AI-Assisted Engineering & Dynamic Pipeline)
=============================================================================
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))


def add_round_rect(slide, left, top, width, height, fill_hex, line_hex=None, line_pt=1.0, radius=0.025):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    if len(shape.adjustments) > 0:
        shape.adjustments[0] = radius
    shape.fill.solid()
    shape.fill.fore_color.rgb = hex_to_rgb(fill_hex)
    if line_hex:
        shape.line.color.rgb = hex_to_rgb(line_hex)
        shape.line.width = Pt(line_pt)
    else:
        shape.line.fill.background()
    return shape


def add_text_box(slide, left, top, width, height, lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """
    lines: list of tuples (text, font_size_pt, color_hex, is_bold, space_after_pt)
    """
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Pt(2)
    tf.margin_right = Pt(2)
    tf.margin_top = Pt(1)
    tf.margin_bottom = Pt(1)

    for idx, item in enumerate(lines):
        text, size_pt, color_hex, is_bold = item[0], item[1], item[2], item[3]
        space_after = item[4] if len(item) > 4 else 2
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = text
        p.alignment = align
        p.space_after = Pt(space_after)
        p.font.name = "Microsoft JhengHei"
        p.font.size = Pt(size_pt)
        p.font.bold = is_bold
        p.font.color.rgb = hex_to_rgb(color_hex)
    return tb


def add_header(slide, title_text, subtitle_text, category_text="SEMICONDUCTOR FAB LOGISTICS INTELLIGENCE"):
    # Category Tag
    add_text_box(
        slide,
        Inches(0.75), Inches(0.32), Inches(11.8), Inches(0.28),
        [(category_text.upper(), 9.5, '38BDF8', True, 0)],
        align=PP_ALIGN.LEFT
    )
    # Main Title
    add_text_box(
        slide,
        Inches(0.75), Inches(0.58), Inches(11.8), Inches(0.52),
        [(title_text, 22, 'FFFFFF', True, 0)],
        align=PP_ALIGN.LEFT
    )
    # Subtitle
    add_text_box(
        slide,
        Inches(0.75), Inches(1.10), Inches(11.8), Inches(0.36),
        [(subtitle_text, 12, '94A3B8', False, 0)],
        align=PP_ALIGN.LEFT
    )


def setup_background(slide, prs):
    # Deep Dark Tech Background
    bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_rect.fill.solid()
    bg_rect.fill.fore_color.rgb = hex_to_rgb('070F1C')
    bg_rect.line.fill.background()

    bg_clean_path = os.path.abspath('scratch/ppt_bg_clean.png')
    if os.path.exists(bg_clean_path):
        slide.shapes.add_picture(bg_clean_path, Inches(0.35), Inches(0.25), Inches(12.633), Inches(7.0))


def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    col_top = Inches(1.60)
    col_h = Inches(5.45)

    # =========================================================================
    # SLIDE 1: 高階主管報告摘要 (Executive Summary: 痛點 vs. 方案三 100% 突破效益)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    setup_background(s1, prs)
    add_header(
        s1,
        "01 ｜ 高階主管報告摘要：營運痛點診斷 vs. 方案三 100% 滿分通過",
        "以原基準缺陷診斷為基石，透過兩階段演算法重構，達成 0 資本支出、運能擴增 29.6% 與 100.0 分合規裁決",
        "EXECUTIVE SUMMARY & OPERATIONAL BREAKTHROUGH"
    )

    # Column 1: 原基準營運痛點 (Baseline: 61.1分 FAILED)
    c1_left = Inches(0.75)
    c1_w = Inches(3.60)
    add_round_rect(s1, c1_left, col_top, c1_w, col_h, '101C2E', 'EF4444', 1.2, radius=0.03)
    
    # Title & Badge
    add_text_box(
        s1, c1_left + Inches(0.15), col_top + Inches(0.12), c1_w - Inches(0.3), Inches(0.38),
        [("【原基準營運痛點診斷】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )
    # Verdict Badge
    add_round_rect(s1, c1_left + Inches(0.4), col_top + Inches(0.50), c1_w - Inches(0.8), Inches(0.40), '3B141E', 'EF4444', 1.0, radius=0.1)
    add_text_box(
        s1, c1_left + Inches(0.4), col_top + Inches(0.53), c1_w - Inches(0.8), Inches(0.35),
        [("🔴 綜合評分: 61.1 分 ｜ 裁決: FAILED", 11, 'FCA5A5', True, 0)],
        align=PP_ALIGN.CENTER
    )

    # 4 Major Pain Points
    pains = [
        ("走廊嚴重超載 (利用率達 200%)", "22 條走廊有 11 條超出 85% 上限，8F➔8S 需求 858 批/供給僅 429 批，嚴重斷料滯留。"),
        ("碼頭進站衝突密集 (8 次嚴重回堵)", "進站班距 < 10 分鐘，多車同時擠入同一泊位，引發廠區主幹道排隊回堵。"),
        ("物理行車時間壓縮 (62 處違規)", "站點間排程時間低於園區物理極限（跨廠需 10~15m 僅排 5m），忽視司機工安。"),
        ("外包廠違規休息 & 佔用泊位", "司機於嘉晶外包廠休息，且用餐時佔據裝卸泊位，違反勞安法規與作業規範。")
    ]
    p_top = col_top + Inches(1.02)
    for p_title, p_desc in pains:
        add_round_rect(s1, c1_left + Inches(0.15), p_top, c1_w - Inches(0.3), Inches(0.96), '152438', '2B4C6F', 1.0, radius=0.04)
        add_text_box(
            s1, c1_left + Inches(0.22), p_top + Inches(0.06), c1_w - Inches(0.44), Inches(0.86),
            [
                (f"• {p_title}", 11, 'F87171', True, 2),
                (p_desc, 9.5, 'CBD5E1', False, 0)
            ]
        )
        p_top += Inches(1.06)

    # Column 2: 方案三突破性成果 (Plan 3: 100.0分 PASSED)
    c2_left = Inches(4.50)
    c2_w = Inches(4.85)
    add_round_rect(s1, c2_left, col_top, c2_w, col_h, '101C2E', '10B981', 1.5, radius=0.03)

    # Title & Badge
    add_text_box(
        s1, c2_left + Inches(0.15), col_top + Inches(0.12), c2_w - Inches(0.3), Inches(0.38),
        [("【方案三：落地成果與突破性效益】", 14, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )
    add_round_rect(s1, c2_left + Inches(0.6), col_top + Inches(0.50), c2_w - Inches(1.2), Inches(0.40), '064E3B', '10B981', 1.2, radius=0.1)
    add_text_box(
        s1, c2_left + Inches(0.6), col_top + Inches(0.53), c2_w - Inches(1.2), Inches(0.35),
        [("🟢 綜合評分: 100.0 / 100 滿分 ｜ 裁決: PASSED", 11.5, '6EE7B7', True, 0)],
        align=PP_ALIGN.CENTER
    )

    # 4 Highlight Metric Cards (2x2 Grid)
    kpis = [
        ("全網有效總運能", "7,776 批/天", "原基準 6,000 批 ➔ 擴增 +29.6%", '34D399', '064E3B'),
        ("走廊最高利用率", "84.7%", "原基準 200.0% ➔ 全數 ≤85.0%", '38BDF8', '0C4A6E'),
        ("碼頭進站衝突數", "0 件 (歸零)", "班距 100% ≥10 分鐘 (原 8 件)", 'FBBF24', '451A03'),
        ("全網無效等待 (Slack)", "0 分鐘/日", "消除全部浪費 (原 60 分鐘)", 'A78BFA', '2E1065')
    ]
    grid_top = col_top + Inches(1.02)
    card_w = Inches(2.22)
    card_h = Inches(1.50)
    for idx, (k_name, k_val, k_sub, col_fg, col_bg) in enumerate(kpis):
        gx = c2_left + Inches(0.15) if idx % 2 == 0 else c2_left + Inches(2.48)
        gy = grid_top if idx < 2 else grid_top + Inches(1.58)
        add_round_rect(s1, gx, gy, card_w, card_h, col_bg, col_fg, 1.2, radius=0.06)
        add_text_box(
            s1, gx + Inches(0.10), gy + Inches(0.12), card_w - Inches(0.20), card_h - Inches(0.20),
            [
                (k_name, 10.5, 'FFFFFF', True, 3),
                (k_val, 19, col_fg, True, 3),
                (k_sub, 9, 'E2E8F0', False, 0)
            ],
            align=PP_ALIGN.CENTER
        )

    # Driver & Dock Protocol Compliance Card (Bottom of Col 2)
    p_bot_top = grid_top + Inches(3.22)
    p_bot_h = col_h - Inches(3.35)
    add_round_rect(s1, c2_left + Inches(0.15), p_bot_top, c2_w - Inches(0.3), p_bot_h, '132338', '3B82F6', 1.0, radius=0.04)
    add_text_box(
        s1, c2_left + Inches(0.25), p_bot_top + Inches(0.10), c2_w - Inches(0.5), p_bot_h - Inches(0.2),
        [
            ("司機休息與碼頭泊位清空管理落實：", 11.5, '93C5FD', True, 3),
            ("• 法定 60 分鐘午晚餐/交接足額保障，全面杜絕疲勞駕駛與超速趕工。", 10, 'E2E8F0', False, 2),
            ("• 休息時車輛必須移至本廠專屬停車區或休息室，絕不佔據碼頭作業泊位。", 10, 'E2E8F0', False, 2),
            ("• 嚴格禁止於外包廠（嘉晶）休息，徹底合規半導體代工資安與廠區管理規章。", 10, 'E2E8F0', False, 0)
        ]
    )

    # Column 3: 經營戰略價值與管理建議 (Strategic Decisions)
    c3_left = Inches(9.50)
    c3_w = Inches(3.10)
    add_round_rect(s1, c3_left, col_top, c3_w, col_h, '101C2E', 'F59E0B', 1.2, radius=0.03)

    add_text_box(
        s1, c3_left + Inches(0.15), col_top + Inches(0.12), c3_w - Inches(0.3), Inches(0.38),
        [("【戰略價值與管理決策】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    strat_cards = [
        ("零資本支出 (CAPEX = $0)", "維持 5 部常態車隊（排除 Car U），完全無需添購新車或額外聘僱司機，淨效益最大化。", '10B981', '064E3B'),
        ("安全抗震裕度 ≥ 15%", "全網 22 條走廊利用率全數 ≤85.0%，足以吸收每日突發急件、機台當機回補與異常波動。", '38BDF8', '0C4A6E'),
        ("建議立即核准正式上線", "方案三各項硬約束 100% 合規、軟約束 100 分，建議運籌生管部門立即啟動新時刻表上線作業。", 'FBBF24', '451A03'),
        ("日常維護：Excel 動態重算", "生管需求變更時，直接於戰情室拖曳上傳 Demand_from_to.xlsx，5 秒全自動完成重新排程。", 'A78BFA', '2E1065')
    ]
    st_top = col_top + Inches(0.55)
    for st_title, st_desc, fg_c, bg_c in strat_cards:
        add_round_rect(s1, c3_left + Inches(0.12), st_top, c3_w - Inches(0.24), Inches(1.15), bg_c, fg_c, 1.0, radius=0.04)
        add_text_box(
            s1, c3_left + Inches(0.20), st_top + Inches(0.08), c3_w - Inches(0.40), Inches(1.02),
            [
                (st_title, 11, fg_c, True, 2),
                (st_desc, 9.5, 'E2E8F0', False, 0)
            ]
        )
        st_top += Inches(1.22)


    # =========================================================================
    # SLIDE 2: 系統規格與數學約束模型 (System Specifications & Math Formulation)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    setup_background(s2, prs)
    add_header(
        s2,
        "02 ｜ 系統規格與數學約束模型：雙層路網與剛性/彈性約束定義",
        "定義半導體多廠區運籌邊界條件，建構 6 大剛性硬約束、2 大品質軟約束與雙目標函數",
        "SYSTEM SPECIFICATIONS & MATHEMATICAL FORMULATION"
    )

    # Column 1: 實體物理環境與雙層路網 (Tier 1 & Tier 2)
    s2_c1_w = Inches(3.70)
    add_round_rect(s2, Inches(0.75), col_top, s2_c1_w, col_h, '101C2E', '38BDF8', 1.2, radius=0.03)
    add_text_box(
        s2, Inches(0.85), col_top + Inches(0.12), s2_c1_w - Inches(0.2), Inches(0.38),
        [("【實體環境與雙層路網架構】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    env_items = [
        ("節點與車隊資源", "• 7 大廠區節點 (8AB/8CD/8E/8F/8S/嘉晶篤行/嘉晶創新)\n• 5 部 3.5 噸箱型車 (Car A~E)，單車物理容量 48 批 (4籠×12)\n• 24H 雙班鏡像：日班 07:35~19:35 / 夜班 19:35~07:35\n• 全網日搬運需求：22 條走廊合計 5,742 批/天"),
        ("第一層：點對點滿載專車 (Express)", "• 專門服務大宗走廊 (如 8F➔8S, 8AB➔8F, 8CD➔8F 等)\n• 單趟滿載 48 批，裝卸時間 15 分鐘，直達目的地全卸\n• 全日配置 72 專車站次，提供高達 6,912 批/天骨幹運能"),
        ("第二層：歐拉環廠滾動承載 (Rolling)", "• 兼顧中小批量跨廠需求，採滾動承載協議：\n  - 首站滿載 48 批 (往後第一站36批 + 往後第二站12批)\n  - 途中各站上貨 24 批 (各12批)，車上保底留空 ≥24 批\n  - 倒數第二站滿車 48 批直達末站全卸，全日 12 站次")
    ]
    e_top = col_top + Inches(0.55)
    for e_title, e_desc in env_items:
        e_h = Inches(1.55)
        add_round_rect(s2, Inches(0.85), e_top, s2_c1_w - Inches(0.2), e_h, '142338', '2563EB', 1.0, radius=0.04)
        add_text_box(
            s2, Inches(0.95), e_top + Inches(0.08), s2_c1_w - Inches(0.4), e_h - Inches(0.16),
            [
                (e_title, 11, '60A5FA', True, 3),
                (e_desc, 9.5, 'E2E8F0', False, 0)
            ]
        )
        e_top += Inches(1.63)

    # Column 2: 六大剛性硬約束 (Hard Constraints 1~6)
    s2_c2_left = Inches(4.60)
    s2_c2_w = Inches(4.55)
    add_round_rect(s2, s2_c2_left, col_top, s2_c2_w, col_h, '101C2E', '10B981', 1.2, radius=0.03)
    add_text_box(
        s2, s2_c2_left + Inches(0.15), col_top + Inches(0.12), s2_c2_w - Inches(0.3), Inches(0.38),
        [("【六大剛性硬約束 (Hard Constraints)】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    hard_rules = [
        ("RULE-HARD-1", "車輛容量極限", "車輛在任何在途路段之總負載嚴格 ≤ 48 批，嚴禁超載。"),
        ("RULE-HARD-2", "環廠滾動協議", "首站滿載 48 / 途中保底空位 ≥24 / 倒數第二站 48 批直達末站。"),
        ("RULE-HARD-3", "走廊頻率保底", "22 條需求走廊每 12 小時班次訪問次數 N ≥ 1 趟，杜絕斷料。"),
        ("RULE-HARD-4", "利用率紅線 ≤85%", "各走廊需求/供給利用率全數 ≤ 85.0%，保留 ≥15% 安全裕度。"),
        ("RULE-HARD-5", "司機休息與停放", "午晚餐/交接 60 分鐘；外包廠禁休；移至專屬停車區不佔泊位。"),
        ("RULE-HARD-6", "物理時間不可壓縮", "廠間通行 (5~15m) 與裝卸作業 (5~15m) 為實體剛性，嚴禁壓縮。")
    ]
    h_top = col_top + Inches(0.55)
    for r_code, r_title, r_desc in hard_rules:
        add_round_rect(s2, s2_c2_left + Inches(0.12), h_top, s2_c2_w - Inches(0.24), Inches(0.76), '132838', '059669', 1.0, radius=0.03)
        add_text_box(
            s2, s2_c2_left + Inches(0.20), h_top + Inches(0.06), s2_c2_w - Inches(0.40), Inches(0.66),
            [
                (f"[{r_code}] {r_title}", 11, '34D399', True, 2),
                (r_desc, 9.5, 'E2E8F0', False, 0)
            ]
        )
        h_top += Inches(0.81)

    # Column 3: 兩大軟約束與雙目標函數 (Soft Constraints & Objectives)
    s2_c3_left = Inches(9.30)
    s2_c3_w = Inches(3.30)
    add_round_rect(s2, s2_c3_left, col_top, s2_c3_w, col_h, '101C2E', 'F59E0B', 1.2, radius=0.03)
    add_text_box(
        s2, s2_c3_left + Inches(0.15), col_top + Inches(0.12), s2_c3_w - Inches(0.3), Inches(0.38),
        [("【軟約束指標與雙目標函數】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    soft_and_obj = [
        ("RULE-SOFT-1 碼頭進站班距", "同一碼頭任意兩車抵達間隔必須 ≥ 10 分鐘，消除碼頭排隊與泊位佔用。方案三達成 0 衝突 (100.0 分)。", 'FBBF24', '451A03'),
        ("RULE-SOFT-2 出發目的地不重複", "同一廠區連續兩班次開往不同目的地，促進跨廠空間多向分流。方案三達成 0 警告 (100.0 分)。", 'FCD34D', '3B2B10'),
        ("目標函數 1：Min Slack (空檔=0)", "最小化車隊全網無效空檔時間：\nmin ∑ Slack_{c,i} = 0 分鐘\n消除任何司機怠速浪費，工時利用最大化。", 'A78BFA', '2E1065'),
        ("目標函數 2：Min 加權等候時間", "最小化晶圓在製品需求加權等候：\nmin ∑ (Wait_{o,d} × Demand_{o,d}) / ∑ Demand\n全網晶圓平均等候時間壓降至 44.3~75.7 分。", '818CF8', '1E1B4B')
    ]
    so_top = col_top + Inches(0.55)
    for so_title, so_desc, fg_c, bg_c in soft_and_obj:
        add_round_rect(s2, s2_c3_left + Inches(0.12), so_top, s2_c3_w - Inches(0.24), Inches(1.15), bg_c, fg_c, 1.0, radius=0.04)
        add_text_box(
            s2, s2_c3_left + Inches(0.20), so_top + Inches(0.08), s2_c3_w - Inches(0.40), Inches(1.02),
            [
                (so_title, 11, fg_c, True, 2),
                (so_desc, 9.5, 'E2E8F0', False, 0)
            ]
        )
        so_top += Inches(1.22)


    # =========================================================================
    # SLIDE 3: 兩階段解耦演算法架構 (Two-Stage Decoupling Architecture)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    setup_background(s3, prs)
    add_header(
        s3,
        "03 ｜ 兩階段解耦演算法架構：空間拓撲趟數與時序防撞排程求解",
        "化解 10³⁵ 狀態空間爆炸：Stage 1 (MILP 歐拉雙層路網) ➔ Stage 2 (CP-SAT 碼頭互斥時序求解)",
        "TWO-STAGE DECOUPLING ALGORITHMIC ARCHITECTURE"
    )

    # Column 1: 複雜度瓶頸與解耦架構 (Why Decouple?)
    s3_c1_w = Inches(3.60)
    add_round_rect(s3, Inches(0.75), col_top, s3_c1_w, col_h, '101C2E', 'EF4444', 1.2, radius=0.03)
    add_text_box(
        s3, Inches(0.85), col_top + Inches(0.12), s3_c1_w - Inches(0.2), Inches(0.38),
        [("【複雜度瓶頸：為何傳統暴力必敗？】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    c_box_top = col_top + Inches(0.55)
    why_items = [
        ("多重 NP-Hard 複合特徵", "本問題同時包含多商品網路流 (MCF)、雙層路網歐拉迴路 (Eulerian Path) 與累積資源時序排程 (Cumulative Scheduling)，端到端決策空間超過 10³⁵ 種狀態，傳統整數規劃直接求解將陷入組合爆炸。"),
        ("人腦經驗與啟發式死鎖", "人工手動微調單一站點時間，即引發下游碼頭跨車連鎖衝突；傳統 GA/遺傳算法難以保證 100% 遵守 6 大剛性硬約束。"),
        ("核心破局策略：兩階段解耦", "將『空間路網趟數分配 (拓撲層)』與『時間軸防撞時序調度 (時序層)』解耦分治，從根本化解維度災難，收斂時間自數小時降至 3~5 秒。")
    ]
    for w_title, w_desc in why_items:
        w_h = Inches(1.55)
        add_round_rect(s3, Inches(0.85), c_box_top, s3_c1_w - Inches(0.2), w_h, '1A1528', 'F43F5E', 1.0, radius=0.04)
        add_text_box(
            s3, Inches(0.95), c_box_top + Inches(0.08), s3_c1_w - Inches(0.4), w_h - Inches(0.16),
            [
                (w_title, 11, 'FDA4AF', True, 3),
                (w_desc, 9.5, 'E2E8F0', False, 0)
            ]
        )
        c_box_top += Inches(1.63)

    # Column 2: 階段一：MILP 歐拉雙層路網趟數分配 (Stage 1)
    s3_c2_left = Inches(4.50)
    s3_c2_w = Inches(4.30)
    add_round_rect(s3, s3_c2_left, col_top, s3_c2_w, col_h, '101C2E', '38BDF8', 1.2, radius=0.03)
    add_text_box(
        s3, s3_c2_left + Inches(0.15), col_top + Inches(0.12), s3_c2_w - Inches(0.3), Inches(0.38),
        [("【階段一：MILP 歐拉雙層路網趟數分配】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    s1_steps = [
        ("1. 需求下界解析 (Capacity Lower Bound)", "依利用率 ≤85% 剛性要求，計算 22 條走廊單班最低運能：\nC_min(o,d) = ceil( Demand_24h(o,d) / 1.70 )\n精確鎖定每條走廊不可打破之供給門檻。"),
        ("2. 歐拉閉迴路度數守恆 (Eulerian Conservation)", "為確保 5 部車在 12H 班末能無縫返回母港交接，全網各廠區之進出度數必須完全相等：\n∑_u X_{u,v} = ∑_w X_{v,w}  (∀ 廠區 v)"),
        ("3. 雙層路網精確配比 (84 站點分配)", "求解混合整數線性規劃 (MILP)，配置 12 站環廠滾動承載 + 72 站滿載專車 = 84 站載貨站，100% 運能精準投放於 22 條需求走廊，無效空跑歸零。")
    ]
    s1_top = col_top + Inches(0.55)
    for st_t, st_d in s1_steps:
        st_h = Inches(1.55)
        add_round_rect(s3, s3_c2_left + Inches(0.12), s1_top, s3_c2_w - Inches(0.24), st_h, '0C2A4A', '0284C7', 1.0, radius=0.04)
        add_text_box(
            s3, s3_c2_left + Inches(0.20), s1_top + Inches(0.08), s3_c2_w - Inches(0.40), st_h - Inches(0.16),
            [
                (st_t, 11, '7DD3FC', True, 3),
                (st_d, 9.5, 'E2E8F0', False, 0)
            ]
        )
        s1_top += Inches(1.63)

    # Column 3: 階段二：CP-SAT 碼頭互斥時序求解 (Stage 2 & Validator)
    s3_c3_left = Inches(8.95)
    s3_c3_w = Inches(3.65)
    add_round_rect(s3, s3_c3_left, col_top, s3_c3_w, col_h, '101C2E', '10B981', 1.2, radius=0.03)
    add_text_box(
        s3, s3_c3_left + Inches(0.15), col_top + Inches(0.12), s3_c3_w - Inches(0.3), Inches(0.38),
        [("【階段二：CP-SAT 碼頭互斥時序求解】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    s2_steps = [
        ("1. Google OR-Tools CP-SAT 區間建模", "建立整數時間變數 IntervalVar(arr, dep, dwell)；為各碼頭設定 AddNoOverlap 約束，強制兩車進站間隔 ≥ 10 分鐘。"),
        ("2. 跨車微創搜尋 (Micro-Jitter Search)", "針對發車時間進行 ±3~5 分鐘微創擾動，利用專車裝卸時間彈性 (Dwell Absorption) 吸收衝突，達成 Slack = 0 分鐘。"),
        ("3. 獨立驗證引擎 (Stage 3 Validator)", "獨立模組 validator.py 以客觀裁判角度逐筆校驗 198 站次時間與容量，生成 audit_report_plan3.html 與 JSON 報告。")
    ]
    s2_top = col_top + Inches(0.55)
    for st_t, st_d in s2_steps:
        st_h = Inches(1.55)
        add_round_rect(s3, s3_c3_left + Inches(0.12), s2_top, s3_c3_w - Inches(0.24), st_h, '064E3B', '10B981', 1.0, radius=0.04)
        add_text_box(
            s3, s3_c3_left + Inches(0.20), s2_top + Inches(0.08), s3_c3_w - Inches(0.40), st_h - Inches(0.16),
            [
                (st_t, 11, '6EE7B7', True, 3),
                (st_d, 9.5, 'E2E8F0', False, 0)
            ]
        )
        s2_top += Inches(1.63)


    # =========================================================================
    # SLIDE 4: AI 工具鏈端到端解題方法論 (AI-Assisted Engineering Methodology)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    setup_background(s4, prs)
    add_header(
        s4,
        "04 ｜ AI 工具鏈賦能：從演算法選型到生產級交付全流程實踐",
        "運用 Antigravity AI Agent 進行語意約束轉化、數學建模、生產級代碼編寫、自我反思與動態管線研發",
        "AI-ASSISTED METHODOLOGY & PRODUCTION-READY ENGINEERING"
    )

    # 4 Columns Layout (Width 2.85 in each)
    p_w = Inches(2.85)
    p_gap = Inches(0.18)
    p_left_base = Inches(0.75)

    pillars = [
        (
            "1. 敏捷選型與約束工程",
            "CONSTRAINT INGESTION",
            "• 非結構化文字轉數學規範：自動解析《問題敘述_限制條件.txt》，提煉出 6 大硬約束 + 2 大軟約束。\n• 邊界痛點診斷：AI 快速辨識出原班表 73 處違規（超載200%、行車壓縮62處），確立兩階段解耦架構。\n• 避開傳統長達數月之需求調研與人工建模週期。",
            '38BDF8', '0C2A4A'
        ),
        (
            "2. 數學建模與程式碼生成",
            "CODEBASE GENERATION",
            "• 混合整數規劃與 CP-SAT 落地：AI 直接編寫 Python 求解器，構建 198 站次行車指南與裝卸指令。\n• 全端架構自底向上建置：生成正規化 SQLite (logistics.db)、非同步雙棧 Web API 伺服器 (server.py)。\n• 前端現代化戰情室：即時渲染甘特圖、廠區分析、SQL 控制台與方案對比頁。",
            '34D399', '064E3B'
        ),
        (
            "3. 自我修復與動態管線",
            "SELF-CORRECTION & PIPELINE",
            "• 裁判與選手分離：獨立撰寫 validator.py 稽核引擎，杜絕演算法自驗自明之盲點。\n• 反思修復閉環：依據驗證器反饋，自動啟動微創搜尋與裝卸吸收，將軟約束警告歸零 (100.0 分)。\n• 動態 Excel 上傳管線：實作 demand_importer.py，支援使用者自訂 Excel 5 秒全自動重新排程。",
            'FBBF24', '451A03'
        ),
        (
            "4. 工程審查自動化護欄",
            "AUTOMATED REVIEW GATES",
            "• CHK-R01 Code Review：廠區命名 100% 精簡標準化 (8AB大廳/8CD碼頭)，AST 跨表結構檢驗通過。\n• CHK-R02 Security Review：SQL 查詢 100% 參數化防注入、路徑白名單防範遍歷、無憑證洩露。\n• CHK-R03 UI&UX Review：深色玻璃擬態對比清晰、拖曳上傳流暢、離線/連線雙模自適應。",
            'A78BFA', '2E1065'
        )
    ]

    for idx, (p_title, p_sub, p_body, fg_c, bg_c) in enumerate(pillars):
        px = p_left_base + idx * (p_w + p_gap)
        add_round_rect(s4, px, col_top, p_w, col_h, '101C2E', fg_c, 1.2, radius=0.03)
        
        # Pillar Header Card
        add_round_rect(s4, px + Inches(0.10), col_top + Inches(0.12), p_w - Inches(0.20), Inches(0.72), bg_c, fg_c, 1.0, radius=0.04)
        add_text_box(
            s4, px + Inches(0.14), col_top + Inches(0.16), p_w - Inches(0.28), Inches(0.64),
            [
                (p_title, 11.5, 'FFFFFF', True, 2),
                (p_sub, 8.5, fg_c, True, 0)
            ],
            align=PP_ALIGN.CENTER
        )

        # Pillar Content Card
        add_round_rect(s4, px + Inches(0.10), col_top + Inches(0.92), p_w - Inches(0.20), col_h - Inches(1.04), '142338', '2B4C6F', 1.0, radius=0.03)
        add_text_box(
            s4, px + Inches(0.18), col_top + Inches(1.04), p_w - Inches(0.36), col_h - Inches(1.24),
            [
                (p_body, 10, 'E2E8F0', False, 0)
            ]
        )

    # Save Presentation
    prs.save(output_path)
    print(f"--> 成功生成可編輯簡報：{output_path}")


if __name__ == '__main__':
    out_file = '半導體廠區物流排程優化_高階主管報告與演算法規格.pptx'
    build_presentation(out_file)
    # 同步複製一份至使用者常用命名路徑
    shutil_copy = '現況診斷與運籌痛點分析_可編輯簡報.pptx'
    print("簡報建構完成！")
