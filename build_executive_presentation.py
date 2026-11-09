# -*- coding: utf-8 -*-
"""
=============================================================================
半導體廠區物流排程優化 - 高階主管報告與演算法規格 簡報生成器 (高階經理人專業版)
=============================================================================
排版規範：
  1. 16:9 寬螢幕高階深色科技風格 (Dark-Tech Boardroom Theme, #070F1C)
  2. 5 頁核心經理人邏輯：
     - Slide 1: 管理層摘要：營運痛點診斷 vs. 新排程落地效益 (0 資本支出 / 100 分合規)
     - Slide 2: 實戰壓力驗證：產能突發變動下的動態調度能力 (5,542 批突變實戰)
     - Slide 3: 運籌架構：7 大廠區雙層路網與現場剛性限制 (車容 / 碼頭 / 用餐法規)
     - Slide 4: 演算法核心：空間拓撲規劃 (MILP) 與碼頭防撞時序 (CP-SAT) (雙層解耦)
     - Slide 5: 交付模式革新：傳統 IT 瀑布流 vs. 現代化敏捷落地 (管理價值與自主重排)
  3. 語言風格：去除所有浮誇宣傳與 AI 味，回歸半導體現場運籌、生管排程與高階決策語言。
=============================================================================
"""

import os
import sys
import shutil
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
    # SLIDE 1: 管理層摘要：營運痛點診斷 vs. 新排程落地效益 (Executive Summary)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    setup_background(s1, prs)
    add_header(
        s1,
        "01 ｜ 管理層摘要：營運痛點診斷 vs. 新排程落地效益",
        "以現況真實缺陷診斷為基準，透過兩階段演算法重構，達成 0 資本支出、運能擴增 29.6% 與 100.0 分合規上線",
        "EXECUTIVE SUMMARY & OPERATIONAL BREAKTHROUGH"
    )

    # Column 1: 原基準營運痛點 (Baseline: 61.1分 FAILED)
    c1_left = Inches(0.75)
    c1_w = Inches(3.60)
    add_round_rect(s1, c1_left, col_top, c1_w, col_h, '101C2E', 'EF4444', 1.2, radius=0.03)
    
    add_text_box(
        s1, c1_left + Inches(0.15), col_top + Inches(0.12), c1_w - Inches(0.3), Inches(0.38),
        [("【原基準營運痛點診斷】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )
    add_round_rect(s1, c1_left + Inches(0.4), col_top + Inches(0.50), c1_w - Inches(0.8), Inches(0.40), '3B141E', 'EF4444', 1.0, radius=0.1)
    add_text_box(
        s1, c1_left + Inches(0.4), col_top + Inches(0.53), c1_w - Inches(0.8), Inches(0.35),
        [("🔴 綜合評分: 61.1 分 ｜ 裁決: FAILED", 11, 'FCA5A5', True, 0)],
        align=PP_ALIGN.CENTER
    )

    pains = [
        ("走廊嚴重超載 (利用率達 200%)", "22 條走廊有 11 條超出 85% 上限，8F➔8S 需求 858 批/供給僅 429 批，引發在製品嚴重滯留。"),
        ("碼頭進站衝突密集 (8 次嚴重回堵)", "進站班距 < 10 分鐘，多車同時擠入同一碼頭，引發廠區主幹道排隊回堵。"),
        ("物理行車時間壓縮 (62 處違規)", "站點間排程時間低於園區物理極限（跨廠需 10~15m 僅排 5m），忽視司機工安與行車風險。"),
        ("外包廠違規休息 & 佔用泊位", "司機於嘉晶外包廠休息，且用餐時佔據裝卸泊位，違反勞安法規與廠區管理規範。")
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

    add_text_box(
        s1, c2_left + Inches(0.15), col_top + Inches(0.12), c2_w - Inches(0.3), Inches(0.38),
        [("【優化排程落地成果（方案三）】", 14, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )
    add_round_rect(s1, c2_left + Inches(0.6), col_top + Inches(0.50), c2_w - Inches(1.2), Inches(0.40), '064E3B', '10B981', 1.2, radius=0.1)
    add_text_box(
        s1, c2_left + Inches(0.6), col_top + Inches(0.53), c2_w - Inches(1.2), Inches(0.35),
        [("🟢 綜合評分: 100.0 / 100 滿分 ｜ 裁決: PASSED", 11.5, '6EE7B7', True, 0)],
        align=PP_ALIGN.CENTER
    )

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
        add_round_rect(s1, gx, gy, card_w, card_h, col_bg, col_fg, 1.0, radius=0.04)
        add_text_box(
            s1, gx + Inches(0.12), gy + Inches(0.10), card_w - Inches(0.24), card_h - Inches(0.20),
            [
                (k_name, 10.5, 'E2E8F0', False, 2),
                (k_val, 19, col_fg, True, 2),
                (k_sub, 8.5, 'CBD5E1', False, 0)
            ],
            align=PP_ALIGN.CENTER
        )

    # Policy Enforcement Box
    add_round_rect(s1, c2_left + Inches(0.15), col_top + Inches(4.25), c2_w - Inches(0.3), Inches(1.05), '152438', '2B4C6F', 1.0, radius=0.03)
    add_text_box(
        s1, c2_left + Inches(0.25), col_top + Inches(4.30), c2_w - Inches(0.5), Inches(0.95),
        [
            ("司機休息與碼頭泊位清空管理落實：", 10.5, '38BDF8', True, 2),
            ("• 法定 60 分鐘午晚餐/交接足額保障，全面杜絕疲勞駕駛與超速趕工風險。", 9.5, 'CBD5E1', False, 1),
            ("• 休息時車輛必須移至本廠專屬停車區，嚴禁佔用碼頭作業泊位。", 9.5, 'CBD5E1', False, 1),
            ("• 嚴格禁止於外包廠（嘉晶）休息，落實半導體代工資安與廠區管理規章。", 9.5, 'CBD5E1', False, 0)
        ]
    )

    # Column 3: 戰略價值與管理決策 (Column 3)
    c3_left = Inches(9.50)
    c3_w = Inches(3.10)
    add_round_rect(s1, c3_left, col_top, c3_w, col_h, '101C2E', '38BDF8', 1.2, radius=0.03)
    add_text_box(
        s1, c3_left + Inches(0.15), col_top + Inches(0.12), c3_w - Inches(0.3), Inches(0.38),
        [("【戰略價值與管理決策】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    decisions = [
        ("零資本支出 (CAPEX = $0)", "維持 5 部常態車隊（排除 Car U），完全不買新車、不增聘司機，淨效益最大化。", '10B981', '064E3B'),
        ("安全抗震裕度 ≥ 15%", "全網 22 條走廊利用率全數 ≤85.0%，足以吸收每日突發急件、機台異常與產能波動。", '38BDF8', '0C2A4A'),
        ("建議核准正式上線", "各項硬約束 100% 合規、軟約束滿分，建議運籌生管部門立即啟動新班表上線切換。", 'FBBF24', '451A03'),
        ("日常維護：Excel 動態重算", "生管需求變更時，直接於戰情室匯入 Excel，數秒內全自動完成重排與防撞校驗。", 'A78BFA', '2E1065')
    ]
    d_top = col_top + Inches(0.55)
    for d_title, d_desc, d_fg, d_bg in decisions:
        add_round_rect(s1, c3_left + Inches(0.12), d_top, c3_w - Inches(0.24), Inches(1.10), d_bg, d_fg, 1.0, radius=0.04)
        add_text_box(
            s1, c3_left + Inches(0.18), d_top + Inches(0.06), c3_w - Inches(0.36), Inches(0.98),
            [
                (d_title, 11, d_fg, True, 2),
                (d_desc, 9.2, 'CBD5E1', False, 0)
            ]
        )
        d_top += Inches(1.20)


    # =========================================================================
    # SLIDE 2: 實戰壓力驗證：產能突發變動下的動態調度能力 (Stress-Test & Dynamic Resilience)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    setup_background(s2, prs)
    add_header(
        s2,
        "02 ｜ 實戰壓力驗證：面對產能突發變動的動態調度能力",
        "以日需求自 5,742 變更為 5,542 批為例：系統關鍵價值在於現場隨時可動態重算，免除 IT 漫長排期",
        "OPERATIONAL RESILIENCE & CASE STUDY ｜ DYNAMIC RESILIENCE AGAINST DEMAND SHOCKS"
    )

    s2_w = Inches(3.75)
    s2_gap = Inches(0.29)
    s2_c1_left = Inches(0.75)
    s2_c2_left = s2_c1_left + s2_w + s2_gap
    s2_c3_left = s2_c2_left + s2_w + s2_gap

    # Column 1: 突發情境：需求結構劇烈異動
    add_round_rect(s2, s2_c1_left, col_top, s2_w, col_h, '101C2E', 'F59E0B', 1.2, radius=0.03)
    add_text_box(
        s2, s2_c1_left + Inches(0.15), col_top + Inches(0.12), s2_w - Inches(0.3), Inches(0.35),
        [("【突發情境：需求結構劇烈異動】", 12.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )
    col1_items = [
        ("全廠需求調整 (5,542 批/日)", "各廠訂單與機台產能波動，總需求自 5,742 微幅下修至 5,542 批，但走廊流向分佈發生結構性轉移。"),
        ("走廊 CD➔E 暴增 (103.7% 超載)", "FAB8CD➔8E 需求突增 100 批 (達 473 批/天)，突破原 456 批運力上限，負荷率飆至 103.7% (🚨 嚴重超載)。"),
        ("傳統 IT 系統困境 (延宕數週)", "傳統靜態系統視此為變更需求，重新開會排期需耗費 3~4 週；現場調度只能手動硬塞，導致月台嚴重塞車與斷料。")
    ]
    c1_y = col_top + Inches(0.55)
    for ci_title, ci_desc in col1_items:
        ci_h = Inches(1.35)
        add_round_rect(s2, s2_c1_left + Inches(0.12), c1_y, s2_w - Inches(0.24), ci_h, '1A1F2C', '78350F', 1.0, radius=0.04)
        add_text_box(
            s2, s2_c1_left + Inches(0.18), c1_y + Inches(0.08), s2_w - Inches(0.36), ci_h - Inches(0.16),
            [
                (ci_title, 11, 'FBBF24', True, 3),
                (ci_desc, 9.5, 'CBD5E1', False, 0)
            ]
        )
        c1_y += Inches(1.45)
    add_round_rect(s2, s2_c1_left + Inches(0.12), col_top + col_h - Inches(0.48), s2_w - Inches(0.24), Inches(0.38), '451A03', 'F59E0B', 1.0, radius=0.08)
    add_text_box(
        s2, s2_c1_left + Inches(0.15), col_top + col_h - Inches(0.45), s2_w - Inches(0.3), Inches(0.32),
        [("⚠️ 現況診斷：88.3 分 🟡 WARNING（走廊超載）", 10, 'FCD34D', True, 0)],
        align=PP_ALIGN.CENTER
    )

    # Column 2: 兩階段動態重排求解
    add_round_rect(s2, s2_c2_left, col_top, s2_w, col_h, '101C2E', '0284C7', 1.2, radius=0.03)
    add_text_box(
        s2, s2_c2_left + Inches(0.15), col_top + Inches(0.12), s2_w - Inches(0.3), Inches(0.35),
        [("【動態重排：兩階段數值求解】", 12.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )
    col2_items = [
        ("極限壓力測試與瓶頸快篩", "新需求 Excel 匯入後，系統 5 秒內完成全網 22 條走廊壓力測試，精準定位 CD➔E 運能缺口 17 批。"),
        ("Stage 1 拓撲運能跨線調撥", "演算法自富餘走廊 (FAB8F➔8S) 抽調 192 批運力至 CD➔E，使 CD➔E 運能自 456 擴增至 648 批，負載降至 73.0% 安全綠線。"),
        ("Stage 2 CP-SAT 時序防撞重算", "重新安排全網到離站時序，確保各廠碼頭車距嚴格 ≥10 分鐘，維持用餐離席無碰撞與零等候浪費。")
    ]
    c2_y = col_top + Inches(0.55)
    for c2_title, c2_desc in col2_items:
        c2_h = Inches(1.35)
        add_round_rect(s2, s2_c2_left + Inches(0.12), c2_y, s2_w - Inches(0.24), c2_h, '0C2A4A', '0284C7', 1.0, radius=0.04)
        add_text_box(
            s2, s2_c2_left + Inches(0.18), c2_y + Inches(0.08), s2_w - Inches(0.36), c2_h - Inches(0.16),
            [
                (c2_title, 11, '7DD3FC', True, 3),
                (c2_desc, 9.5, 'E2E8F0', False, 0)
            ]
        )
        c2_y += Inches(1.45)
    add_round_rect(s2, s2_c2_left + Inches(0.12), col_top + col_h - Inches(0.48), s2_w - Inches(0.24), Inches(0.38), '0C4A6E', '38BDF8', 1.0, radius=0.08)
    add_text_box(
        s2, s2_c2_left + Inches(0.15), col_top + col_h - Inches(0.45), s2_w - Inches(0.3), Inches(0.32),
        [("⚡ 兩階段求解：數秒內完成重排並通過防撞校驗", 10, 'BAE6FD', True, 0)],
        align=PP_ALIGN.CENTER
    )

    # Column 3: 高階管理價值：敏捷運籌抗震力
    add_round_rect(s2, s2_c3_left, col_top, s2_w, col_h, '101C2E', '10B981', 1.5, radius=0.03)
    add_text_box(
        s2, s2_c3_left + Inches(0.15), col_top + Inches(0.12), s2_w - Inches(0.3), Inches(0.35),
        [("【高階管理價值：敏捷運籌抗震力】", 12.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )
    col3_items = [
        ("滿分驗收：100.0 分 🟢 PASSED", "走廊最高負荷自 103.7% 降至 84.7%，全網 22 條走廊全部合規 (≤85%)，碼頭衝突維持 0 件。"),
        ("現場自主掌控，擺脫 IT 排期枷鎖", "產能變更是工廠常態；現場生管上傳 Excel 即可一鍵重算，不用再等跨部門開會排期。"),
        ("實質投資回報率 (Strategic ROI)", "最關鍵的價值不是節省開發工時，而是為半導體晶圓廠建立了「不怕產能劇變、不塞車、不斷料」的供應鏈韌性。")
    ]
    c3_y = col_top + Inches(0.55)
    for c3_title, c3_desc in col3_items:
        c3_h = Inches(1.35)
        add_round_rect(s2, s2_c3_left + Inches(0.12), c3_y, s2_w - Inches(0.24), c3_h, '064E3B', '10B981', 1.0, radius=0.04)
        add_text_box(
            s2, s2_c3_left + Inches(0.18), c3_y + Inches(0.08), s2_w - Inches(0.36), c3_h - Inches(0.16),
            [
                (c3_title, 11, '6EE7B7', True, 3),
                (c3_desc, 9.5, 'E2E8F0', False, 0)
            ]
        )
        c3_y += Inches(1.45)
    add_round_rect(s2, s2_c3_left + Inches(0.12), col_top + col_h - Inches(0.48), s2_w - Inches(0.24), Inches(0.38), '064E3B', '10B981', 1.2, radius=0.08)
    add_text_box(
        s2, s2_c3_left + Inches(0.15), col_top + col_h - Inches(0.45), s2_w - Inches(0.3), Inches(0.32),
        [("🏆 管理成果：賦予廠區面對波動的即時調度韌性", 10, 'A7F3D0', True, 0)],
        align=PP_ALIGN.CENTER
    )


    # =========================================================================
    # SLIDE 3: 運籌架構：7 大廠區雙層路網與現場剛性限制 (System Specifications)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    setup_background(s3, prs)
    add_header(
        s3,
        "03 ｜ 運籌架構：7 大廠區雙層路網與現場剛性限制",
        "嚴格定義半導體多廠區作業邊界，建構 6 大剛性硬約束、2 大品質軟約束與雙優化目標",
        "SYSTEM SPECIFICATIONS & OPERATIONAL CONSTRAINTS"
    )

    s3_c1_left = Inches(0.75)
    s3_c1_w = Inches(3.80)
    add_round_rect(s3, s3_c1_left, col_top, s3_c1_w, col_h, '101C2E', '38BDF8', 1.2, radius=0.03)
    add_text_box(
        s3, s3_c1_left + Inches(0.15), col_top + Inches(0.12), s3_c1_w - Inches(0.3), Inches(0.38),
        [("【實體環境與雙層路網架構】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    env_blocks = [
        ("節點與車隊資源", "• 7 大廠區節點 (8AB/8CD/8E/8F/8S/嘉晶篤行/嘉晶創新)\n• 5 部 3.5 噸箱型車 (Car A~E)，單車物理容量 48 批 (4籠×12)\n• 24H 雙班鏡像：日班 07:35~19:35 / 夜班 19:35~07:35\n• 全網日搬運需求：22 條走廊合計 5,742 批/天"),
        ("第一層：點對點滿載專車 (Express)", "• 專門服務大宗走廊 (如 8F➔8S, 8AB➔8F, 8CD➔8F 等)\n• 單趟滿載 48 批，裝卸時間 15 分鐘，直達目的地全卸\n• 全日配置 72 專車站次，提供高達 6,912 批/天骨幹運能"),
        ("第二層：歐拉環廠滾動承載 (Rolling)", "• 兼顧中小批量跨廠需求，採滾動承載協議：\n  - 首站滿載 48 批 (往後第一站36批 + 往後第二站12批)\n  - 途中各站上貨 24 批 (各12批)，車上保底留空 ≥24 批\n  - 倒數第二站滿車 48 批直達末站全卸，全日 12 站次")
    ]
    eb_top = col_top + Inches(0.55)
    for eb_t, eb_d in env_blocks:
        eb_h = Inches(1.50)
        add_round_rect(s3, s3_c1_left + Inches(0.12), eb_top, s3_c1_w - Inches(0.24), eb_h, '142338', '2B4C6F', 1.0, radius=0.04)
        add_text_box(
            s3, s3_c1_left + Inches(0.20), eb_top + Inches(0.08), s3_c1_w - Inches(0.40), eb_h - Inches(0.16),
            [
                (eb_t, 11, '38BDF8', True, 3),
                (eb_d, 9.2, 'CBD5E1', False, 0)
            ]
        )
        eb_top += Inches(1.58)

    # Column 2: 六大剛性硬約束 (Hard Constraints)
    s3_c2_left = Inches(4.75)
    s3_c2_w = Inches(3.90)
    add_round_rect(s3, s3_c2_left, col_top, s3_c2_w, col_h, '101C2E', 'EF4444', 1.2, radius=0.03)
    add_text_box(
        s3, s3_c2_left + Inches(0.15), col_top + Inches(0.12), s3_c2_w - Inches(0.3), Inches(0.38),
        [("【六大剛性硬約束 (Hard Constraints)】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    hards = [
        ("[RULE-HARD-1] 車輛容量極限", "車輛在任何在途路段之總負載嚴格 ≤ 48 批，嚴禁超載。"),
        ("[RULE-HARD-2] 環廠滾動協議", "首站滿載 48 / 途中保底空位 ≥24 / 倒數第二站 48 批直達末站。"),
        ("[RULE-HARD-3] 走廊頻率保底", "22 條需求走廊每 12 小時班次訪問次數 N ≥ 1 趟，杜絕斷料。"),
        ("[RULE-HARD-4] 利用率紅線 ≤85%", "各走廊需求/供給利用率全數 ≤ 85.0%，保留 ≥15% 安全裕度。"),
        ("[RULE-HARD-5] 司機休息與停放", "午晚餐/交接 60 分鐘；外包廠禁休；移至專屬停車區不佔泊位。"),
        ("[RULE-HARD-6] 物理時間不可壓縮", "廠間通行 (5~15m) 與裝卸作業 (5~15m) 為實體剛性，嚴禁壓縮。")
    ]
    h_top = col_top + Inches(0.55)
    for h_t, h_d in hards:
        h_h = Inches(0.74)
        add_round_rect(s3, s3_c2_left + Inches(0.12), h_top, s3_c2_w - Inches(0.24), h_h, '1E1E2E', '7F1D1D', 1.0, radius=0.04)
        add_text_box(
            s3, s3_c2_left + Inches(0.18), h_top + Inches(0.04), s3_c2_w - Inches(0.36), h_h - Inches(0.08),
            [
                (h_t, 10.5, 'FCA5A5', True, 1),
                (h_d, 9.0, 'E2E8F0', False, 0)
            ]
        )
        h_top += Inches(0.79)

    # Column 3: 軟約束指標與雙目標函數
    s3_c3_left = Inches(8.85)
    s3_c3_w = Inches(3.75)
    add_round_rect(s3, s3_c3_left, col_top, s3_c3_w, col_h, '101C2E', '10B981', 1.2, radius=0.03)
    add_text_box(
        s3, s3_c3_left + Inches(0.15), col_top + Inches(0.12), s3_c3_w - Inches(0.3), Inches(0.38),
        [("【軟約束指標與雙目標函數】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    softs = [
        ("RULE-SOFT-1 碼頭進站班距", "同一碼頭任意兩車抵達間隔必須 ≥ 10 分鐘，消除碼頭排隊與泊位佔用。方案三達成 0 衝突 (100.0 分)。", '10B981', '064E3B'),
        ("RULE-SOFT-2 出發目的地不重複", "同一廠區連續兩班次開往不同目的地，促進跨廠空間多向分流。方案三達成 0 警告 (100.0 分)。", '38BDF8', '0C4A6E'),
        ("目標函數 1：Min Slack (空檔=0)", "最小化車隊全網無效空檔時間： min ∑ Slack_i 達成司機工時 100% 緊湊高效，全網等候浪費歸零。", 'FBBF24', '451A03'),
        ("目標函數 2：Min Wait (最小化材料等候時間)", "最小化全廠需求加權預期等候時間： min ∑ Demand_od · E[W_od]，大幅縮短晶圓在途等待，杜絕產線斷料。", 'A78BFA', '2E1065')
    ]
    s_top = col_top + Inches(0.55)
    for s_t, s_d, s_fg, s_bg in softs:
        s_h = Inches(1.12)
        add_round_rect(s3, s3_c3_left + Inches(0.12), s_top, s3_c3_w - Inches(0.24), s_h, s_bg, s_fg, 1.0, radius=0.04)
        add_text_box(
            s3, s3_c3_left + Inches(0.18), s_top + Inches(0.06), s3_c3_w - Inches(0.36), s_h - Inches(0.12),
            [
                (s_t, 11, s_fg, True, 2),
                (s_d, 9.2, 'E2E8F0', False, 0)
            ]
        )
        s_top += Inches(1.20)


    # =========================================================================
    # SLIDE 4: 演算法核心：空間拓撲規劃 (MILP) 與碼頭防撞時序 (CP-SAT)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    setup_background(s4, prs)
    add_header(
        s4,
        "04 ｜ 演算法核心：空間拓撲規劃 (MILP) 與碼頭防撞時序 (CP-SAT)",
        "將大規模 NP-hard 難題解耦為兩階段流水線：Stage 1 求解宏觀趟數分配 + Stage 2 求解微觀防撞排程",
        "TWO-STAGE DECOUPLED OPTIMIZATION ｜ TOPOLOGY ALLOCATION & COLLISION-FREE TIMING"
    )

    s4_c1_left = Inches(0.75)
    s4_c1_w = Inches(3.60)
    add_round_rect(s4, s4_c1_left, col_top, s4_c1_w, col_h, '101C2E', 'F59E0B', 1.2, radius=0.03)
    add_text_box(
        s4, s4_c1_left + Inches(0.15), col_top + Inches(0.12), s4_c1_w - Inches(0.3), Inches(0.38),
        [("【瓶頸破局：為何傳統算法失效？】", 13.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    puzzles = [
        ("單層 VRPTW 算力爆炸 (NP-Hard)", "若將 7 車、24H、7 廠區、22 走廊之「路徑選取、載重分配、發車時序、碼頭互斥」全塞入單一混合整數規劃，變數達 10^7 量級，求解數小時仍記憶體溢出。"),
        ("時空高度耦合之衝突震盪", "只要某一站調整 3 分鐘，後續所有站點抵達時間全數偏移，導致下游碼頭排隊骨牌效應，傳統啟發式算法（如 GA / 模擬退火）極難滿足 100% 硬約束。"),
        ("破局思維：時空解耦分治架構", "將問題拆解為兩階段：先在宏觀層面定好趟數配比 (MILP)，再在微觀層面精準推移發車時間 (CP-SAT)，計算時間自數小時降至 3~5 秒。")
    ]
    puz_top = col_top + Inches(0.55)
    for pz_t, pz_d in puzzles:
        pz_h = Inches(1.55)
        add_round_rect(s4, s4_c1_left + Inches(0.12), puz_top, s4_c1_w - Inches(0.24), pz_h, '1A1F2C', '78350F', 1.0, radius=0.04)
        add_text_box(
            s4, s4_c1_left + Inches(0.20), puz_top + Inches(0.08), s4_c1_w - Inches(0.40), pz_h - Inches(0.16),
            [
                (pz_t, 11, 'FBBF24', True, 3),
                (pz_d, 9.5, 'CBD5E1', False, 0)
            ]
        )
        puz_top += Inches(1.63)

    # Column 2: 階段一：MILP 歐拉雙層路網趟數分配
    s4_c2_left = Inches(4.55)
    s4_c2_w = Inches(4.20)
    add_round_rect(s4, s4_c2_left, col_top, s4_c2_w, col_h, '101C2E', '0284C7', 1.2, radius=0.03)
    add_text_box(
        s4, s4_c2_left + Inches(0.15), col_top + Inches(0.12), s4_c2_w - Inches(0.3), Inches(0.38),
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
        add_round_rect(s4, s4_c2_left + Inches(0.12), s1_top, s4_c2_w - Inches(0.24), st_h, '0C2A4A', '0284C7', 1.0, radius=0.04)
        add_text_box(
            s4, s4_c2_left + Inches(0.20), s1_top + Inches(0.08), s4_c2_w - Inches(0.40), st_h - Inches(0.16),
            [
                (st_t, 11, '7DD3FC', True, 3),
                (st_d, 9.5, 'E2E8F0', False, 0)
            ]
        )
        s1_top += Inches(1.63)

    # Column 3: 階段二：CP-SAT 碼頭互斥時序求解
    s4_c3_left = Inches(8.95)
    s4_c3_w = Inches(3.65)
    add_round_rect(s4, s4_c3_left, col_top, s4_c3_w, col_h, '101C2E', '10B981', 1.2, radius=0.03)
    add_text_box(
        s4, s4_c3_left + Inches(0.15), col_top + Inches(0.12), s4_c2_w - Inches(0.3), Inches(0.38),
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
        add_round_rect(s4, s4_c3_left + Inches(0.12), s2_top, s4_c3_w - Inches(0.24), st_h, '064E3B', '10B981', 1.0, radius=0.04)
        add_text_box(
            s4, s4_c3_left + Inches(0.20), s2_top + Inches(0.08), s4_c3_w - Inches(0.40), st_h - Inches(0.16),
            [
                (st_t, 11, '6EE7B7', True, 3),
                (st_d, 9.5, 'E2E8F0', False, 0)
            ]
        )
        s2_top += Inches(1.63)


    # =========================================================================
    # SLIDE 5: 交付模式革新：傳統 IT 瀑布流 vs. 現代化敏捷落地 (Delivery Paradigm)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    setup_background(s5, prs)
    add_header(
        s5,
        "05 ｜ 交付模式革新：傳統 IT 瀑布流 vs. 現代化敏捷落地",
        "打破「跨 5 部門、耗時半年的多層交接摩擦」，實現「領域專家主導、1 週端到端閉環落地」的管理價值",
        "DELIVERY PARADIGM REVOLUTION ｜ WATERFALL OVERHEAD VS. DOMAIN-LED AGILITY"
    )

    s5_w = Inches(5.75)
    s5_gap = Inches(0.33)
    s5_c1_left = Inches(0.75)
    s5_c2_left = s5_c1_left + s5_w + s5_gap

    # Left Container: 傳統跨部門瀑布模式 (6~9 個月)
    add_round_rect(s5, s5_c1_left, col_top, s5_w, col_h, '101C2E', 'EF4444', 1.2, radius=0.03)
    add_text_box(
        s5, s5_c1_left + Inches(0.2), col_top + Inches(0.12), s5_w - Inches(0.4), Inches(0.35),
        [("【傳統模式：跨部門專業分工（耗時 6~9 個月）】", 13, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    trad_steps = [
        ("1. 現場痛點調研 (耗時 1 個月)", "IE 與生管拿碼表跟車訪談司機、手動記錄月台塞車與貨物滯留，整理業務需求說明書。"),
        ("2. 運籌數學建模 (耗時 1 個月)", "找資料科學家或外包顧問推導公式，常陷入大矩陣算力爆炸 (NP-hard)，難以算出生產級解。"),
        ("3. 提單與 IT 排期 (耗時 2~3 週)", "跨部門開會審核規格、爭取系統開發排期，業務需求常在多次轉譯溝通中失真。"),
        ("4. IT 全端系統編碼 (耗時 2~3 個月)", "IT 前後端分頭寫程式、建資料庫、手刻前台網頁，規格一變即引發嚴重返工摩擦。"),
        ("5. 現場驗收與試跑 (耗時 1 個月)", "現場試跑驗收改 Bug；算出來的班表過於理想化，常被現場司機抱怨根本開不出來。")
    ]
    t_top = col_top + Inches(0.52)
    for st_title, st_desc in trad_steps:
        st_box_h = Inches(0.82)
        add_round_rect(s5, s5_c1_left + Inches(0.15), t_top, s5_w - Inches(0.3), st_box_h, '1A1F2C', '7F1D1D', 1.0, radius=0.03)
        add_text_box(
            s5, s5_c1_left + Inches(0.22), t_top + Inches(0.06), s5_w - Inches(0.44), st_box_h - Inches(0.12),
            [
                (f"• {st_title}", 10.5, 'FCA5A5', True, 2),
                (st_desc, 9.2, 'CBD5E1', False, 0)
            ]
        )
        t_top += Inches(0.88)

    add_round_rect(s5, s5_c1_left + Inches(0.15), col_top + col_h - Inches(0.48), s5_w - Inches(0.3), Inches(0.38), '3B141E', 'EF4444', 1.0, radius=0.08)
    add_text_box(
        s5, s5_c1_left + Inches(0.2), col_top + col_h - Inches(0.45), s5_w - Inches(0.4), Inches(0.32),
        [("🔴 核心痛點：多層交接摩擦、專案週期漫長、需求一變全部重來", 10, 'FCA5A5', True, 0)],
        align=PP_ALIGN.CENTER
    )

    # Right Container: 現代化工程實踐（領域主導敏捷落地，1 週交付）
    add_round_rect(s5, s5_c2_left, col_top, s5_w, col_h, '101C2E', '10B981', 1.5, radius=0.03)
    add_text_box(
        s5, s5_c2_left + Inches(0.2), col_top + Inches(0.12), s5_w - Inches(0.4), Inches(0.35),
        [("【現代敏捷模式：領域主導全鏈落地（< 1 週端到端閉環）】", 13, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER
    )

    ai_steps = [
        ("1. 領域專家直下關鍵規則 (零溝通摩擦)", "懂現場的人直接定義核心限制（司機用餐不佔碼頭、各廠上下貨耗時、轉彎行車時間）。"),
        ("2. 演算法秒級解耦求解 (雙層數值架構)", "自發建構 Stage 1 MILP 拓撲配比 + Stage 2 CP-SAT 時序防撞，徹底避開單層大模型算力爆炸。"),
        ("3. 全端架構一體成型 (代碼即規格)", "同步產出正規化 SQLite、REST API、現代化戰情室、動態甘特圖與廠區時刻表。"),
        ("4. 獨立數位稽核護欄 (客觀裁判防護)", "validator.py 逐班檢驗 198 站次時間與容量，確保 100% 合規不踩雷、無自驗自明盲點。"),
        ("5. 現場自主動態自癒 (隨時驗收與重排)", "現場隨時丟入新需求 Excel，系統自動診斷瓶頸，秒級動態重排並自我修復回 100 分。")
    ]
    a_top = col_top + Inches(0.52)
    for sa_title, sa_desc in ai_steps:
        sa_box_h = Inches(0.82)
        add_round_rect(s5, s5_c2_left + Inches(0.15), a_top, s5_w - Inches(0.3), sa_box_h, '064E3B', '059669', 1.0, radius=0.03)
        add_text_box(
            s5, s5_c2_left + Inches(0.22), a_top + Inches(0.06), s5_w - Inches(0.44), sa_box_h - Inches(0.12),
            [
                (f"• {sa_title}", 10.5, '6EE7B7', True, 2),
                (sa_desc, 9.2, 'E2E8F0', False, 0)
            ]
        )
        a_top += Inches(0.88)

    add_round_rect(s5, s5_c2_left + Inches(0.15), col_top + col_h - Inches(0.48), s5_w - Inches(0.3), Inches(0.38), '064E3B', '10B981', 1.2, radius=0.08)
    add_text_box(
        s5, s5_c2_left + Inches(0.2), col_top + col_h - Inches(0.45), s5_w - Inches(0.4), Inches(0.32),
        [("🟢 核心效益：領域專家掌控全流程，跳過跨部門公文，數天交付生產級系統", 10, 'A7F3D0', True, 0)],
        align=PP_ALIGN.CENTER
    )

    # Save Presentation (Handle file lock if user has PowerPoint open)
    try:
        prs.save(output_path)
        print(f"--> 成功生成可編輯簡報：{output_path}")
    except PermissionError:
        fallback_path = output_path.replace('.pptx', '_new.pptx')
        prs.save(fallback_path)
        print(f"--> 原檔案由 PowerPoint 開啟鎖定中，已成功另存為最新版本：{fallback_path}")


if __name__ == '__main__':
    out_file = '半導體廠區物流排程優化_高階主管報告與演算法規格.pptx'
    build_presentation(out_file)
    shutil_copy = '現況診斷與運籌痛點分析_可編輯簡報.pptx'
    try:
        shutil.copyfile(out_file, shutil_copy)
        print(f"--> 已同步複製更新：{shutil_copy}")
    except Exception as e:
        print(f"同步複製提示（若正在開啟中可稍後同步）: {e}")
    print("簡報建構完成！")
