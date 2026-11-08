# -*- coding: utf-8 -*-
"""
=============================================================================
半導體廠區物流排程優化 - 高階主管簡報與演算法手冊 (全圖表高階可編輯版)
=============================================================================
嚴格對齊參考風格：「現況診斷與運籌痛點分析_可編輯簡報.pptx」
包含五大完整維度：
  Slide 1: 跨廠物流營運現況診斷與痛點分析 (原圖 1:1 復刻與向量圖表化)
  Slide 2: 半導體廠區物流系統規格與數學約束模型 (問題描述、雙層路網、6硬+2軟約束)
  Slide 3: 兩階段解耦演算法架構：拓撲趟數重構與時序防撞排程 (MILP + CP-SAT + 微創搜尋)
  Slide 4: 方案三落地成果與全景突破性效益對比 (100分滿分驗收、KPI 躍升、司機管理)
  Slide 5: 如何利用 Antigravity AI 工具鏈端到端解題 (選型、建模、代碼、動態Excel重算管線)
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
from pptx.enum.dml import MSO_LINE_DASH_STYLE

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


def setup_slide_header(slide, title_text, subtitle_text):
    # Centered Header Matching Reference Image
    add_text_box(
        slide,
        Inches(1.5), Inches(0.40), Inches(10.333), Inches(0.65),
        [(title_text, 28, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )
    add_text_box(
        slide,
        Inches(1.5), Inches(1.05), Inches(10.333), Inches(0.42),
        [(subtitle_text, 15, '7DD3FC', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )


def setup_background(slide, prs):
    bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_rect.fill.solid()
    bg_rect.fill.fore_color.rgb = hex_to_rgb('070F1C')
    bg_rect.line.fill.background()

    bg_clean_path = os.path.abspath('scratch/ppt_bg_clean.png')
    if os.path.exists(bg_clean_path):
        slide.shapes.add_picture(bg_clean_path, Inches(0.35), Inches(0.25), Inches(12.633), Inches(7.0))


def build_full_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    col_top = Inches(1.65)
    col_h = Inches(5.38)

    # =========================================================================
    # SLIDE 1: 跨廠物流營運現況診斷與痛點分析 (1:1 復刻與向量圖表化)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    setup_background(s1, prs)
    setup_slide_header(
        s1,
        "跨廠物流營運現況診斷與痛點分析",
        "半導體多廠區物料轉運與車輛排程瓶頸結構性解構"
    )

    # Column 1: Left Module (核心根因：人工排程瓶頸)
    c1_left = Inches(0.75)
    c1_w = Inches(3.38)
    c1_top_h = Inches(3.85)
    add_round_rect(s1, c1_left, col_top, c1_w, c1_top_h, '101C2E', '2B4C6F', 1.2, radius=0.03)
    add_text_box(
        s1, c1_left + Inches(0.1), col_top + Inches(0.12), c1_w - Inches(0.2), Inches(0.4),
        [("【核心根因：人工排程瓶頸】", 14.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    brain_chip_path = os.path.abspath('scratch/icon_brain_chip.png')
    if os.path.exists(brain_chip_path):
        s1.shapes.add_picture(brain_chip_path, c1_left + Inches(0.16), col_top + Inches(0.58), c1_w - Inches(0.32), Inches(1.38))

    add_text_box(
        s1, c1_left + Inches(0.14), col_top + Inches(2.02), Inches(1.45), Inches(0.52),
        [("人腦線性經驗", 11.5, 'FFFFFF', True, 1), ("片斷直覺手動調度", 9.5, '94A3B8', False, 0)],
        align=PP_ALIGN.CENTER
    )
    add_text_box(
        s1, c1_left + c1_w - Inches(1.68), col_top + Inches(2.02), Inches(1.55), Inches(0.52),
        [("半導體物流網路", 11.5, '7DD3FC', True, 1), ("高維時空全局約束", 9.5, '38BDF8', False, 0)],
        align=PP_ALIGN.CENTER
    )

    var_top = col_top + Inches(2.65)
    var_h = Inches(1.02)
    add_round_rect(s1, c1_left + Inches(0.16), var_top, c1_w - Inches(0.32), var_h, '13253C', '386690', 1.0, radius=0.08)
    add_text_box(
        s1, c1_left + Inches(0.22), var_top + Inches(0.12), c1_w - Inches(0.44), var_h - Inches(0.2),
        [("5 部專用貨車 × 22 條跨廠路線", 12, 'FFFFFF', True, 6), ("198 處停靠站點 × 碼頭泊位限制", 11.5, 'E2E8F0', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    ins_top = col_top + c1_top_h + Inches(0.15)
    ins_h = col_h - c1_top_h - Inches(0.15)
    add_round_rect(s1, c1_left, ins_top, c1_w, ins_h, '3B2B10', 'D97706', 1.5, radius=0.04)
    add_text_box(
        s1, c1_left + Inches(0.15), ins_top + Inches(0.12), c1_w - Inches(0.3), ins_h - Inches(0.2),
        [
            ("【關鍵洞察】", 13.5, 'FBBF24', True, 6),
            ("高維度時空變數組合爆炸，超越人腦認知極限；單一車次微調即引發連鎖排隊，導致被動應付式調度。", 10.5, 'FDE68A', True, 0)
        ],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # Column 2: Middle Module (三大關鍵營運痛點分析)
    c2_left = Inches(4.30)
    c2_w = Inches(5.05)
    add_round_rect(s1, c2_left, col_top, c2_w, col_h, '101C2E', '2B4C6F', 1.2, radius=0.025)
    add_text_box(
        s1, c2_left + Inches(0.15), col_top + Inches(0.12), c2_w - Inches(0.3), Inches(0.4),
        [("【三大關鍵營運痛點分析】", 15, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    row_left = c2_left + Inches(0.14)
    row_w = c2_w - Inches(0.28)

    # Row 1: 18條路線過載 + Histogram Chart
    r1_top = col_top + Inches(0.56)
    r1_h = Inches(1.48)
    add_round_rect(s1, row_left, r1_top, row_w, r1_h, '142338', '2C4A6E', 1.0, radius=0.04)
    add_text_box(s1, row_left + Inches(0.12), r1_top + Inches(0.08), Inches(3.2), Inches(0.32), [("痛點一：18 條路線負荷過載", 12.5, 'FFFFFF', True, 0)])

    chart_base_y = r1_top + Inches(1.32)
    chart_left_x = row_left + Inches(0.18)
    bar_heights_in = [0.24, 0.30, 0.35, 0.32, 0.50, 0.72, 0.32, 0.25, 0.38, 0.44, 0.44, 0.36, 0.42, 0.80]
    bar_step_in = 0.165
    for idx, bh in enumerate(bar_heights_in):
        bx = chart_left_x + Inches(idx * bar_step_in)
        by = chart_base_y - Inches(bh)
        b_col = 'EF4444' if idx == 13 else '38BDF8'
        bar_sh = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, by, Inches(0.115), Inches(bh))
        bar_sh.fill.solid()
        bar_sh.fill.fore_color.rgb = hex_to_rgb(b_col)
        bar_sh.line.fill.background()

    base_ln = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, chart_left_x - Inches(0.04), chart_base_y, Inches(2.38), Inches(0.015))
    base_ln.fill.solid()
    base_ln.fill.fore_color.rgb = hex_to_rgb('94A3B8')
    base_ln.line.fill.background()

    thresh_y = chart_base_y - Inches(0.60)
    for dash_i in range(18):
        dx = chart_left_x - Inches(0.02) + Inches(dash_i * 0.13)
        d_seg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, dx, thresh_y, Inches(0.075), Inches(0.018))
        d_seg.fill.solid()
        d_seg.fill.fore_color.rgb = hex_to_rgb('EF4444')
        d_seg.line.fill.background()

    add_text_box(s1, chart_left_x + Inches(0.92), thresh_y - Inches(0.23), Inches(1.25), Inches(0.22), [("85% 安全警戒線", 8.5, 'F87171', True, 0)], align=PP_ALIGN.RIGHT)
    add_text_box(s1, chart_left_x + Inches(13 * bar_step_in) - Inches(0.14), chart_base_y - Inches(1.02), Inches(0.45), Inches(0.22), [("200%", 9.0, 'EF4444', True, 0)], align=PP_ALIGN.CENTER)
    add_text_box(s1, row_left + Inches(2.68), r1_top + Inches(0.40), row_w - Inches(2.78), Inches(0.95), [("嘉晶外包廠路線負荷達", 11, 'FFFFFF', True, 2), ("200%（天天欠料斷線", 11, 'FCA5A5', True, 2), ("，物料跨班滯留）", 11, 'FFFFFF', True, 0)])

    # Row 2: 痛點二：運輸模式配置僵化 + Circular loop truck icon
    r2_top = r1_top + r1_h + Inches(0.12)
    r2_h = Inches(1.48)
    add_round_rect(s1, row_left, r2_top, row_w, r2_h, '142338', '2C4A6E', 1.0, radius=0.04)
    add_text_box(s1, row_left + Inches(0.12), r2_top + Inches(0.08), Inches(3.2), Inches(0.32), [("痛點二：運輸模式配置僵化", 12.5, 'FFFFFF', True, 0)])

    loop_truck_path = os.path.abspath('scratch/icon_loop_truck.png')
    if os.path.exists(loop_truck_path):
        s1.shapes.add_picture(loop_truck_path, row_left + Inches(0.18), r2_top + Inches(0.36), Inches(2.35), Inches(1.02))

    add_text_box(s1, row_left + Inches(2.68), r2_top + Inches(0.38), row_w - Inches(2.78), Inches(0.98), [("全日 0 趟直達專車；48", 11, 'FFFFFF', True, 2), ("儲位貨車長期低乘載率", 11, 'FDE68A', True, 2), ("，運能嚴重浪費。", 11, 'FFFFFF', True, 0)])

    # Row 3: 痛點三：多車同時到站與服務真空 + 24H Timeline Chart
    r3_top = r2_top + r2_h + Inches(0.12)
    r3_h = Inches(1.56)
    add_round_rect(s1, row_left, r3_top, row_w, r3_h, '142338', '2C4A6E', 1.0, radius=0.04)
    add_text_box(s1, row_left + Inches(0.12), r3_top + Inches(0.08), Inches(2.65), Inches(0.32), [("痛點三：多車同時到站與服務真空", 11.5, 'FFFFFF', True, 0)])

    wip_pill = add_round_rect(s1, row_left + Inches(2.70), r3_top + Inches(0.07), row_w - Inches(2.80), Inches(0.28), '1A2A40', '475569', 1.0, radius=0.25)
    add_text_box(s1, row_left + Inches(2.71), r3_top + Inches(0.07), row_w - Inches(2.82), Inches(0.28), [("晶圓在製品平均等候時間：131.6 分鐘", 7.8, 'FBBF24', True, 0)], align=PP_ALIGN.CENTER)

    tl_left = row_left + Inches(0.22)
    tl_w = row_w - Inches(0.48)
    tl_axis_y = r3_top + Inches(1.22)
    add_text_box(s1, tl_left - Inches(0.05), r3_top + Inches(0.42), Inches(2.52), Inches(0.24), [("8 次碼頭同時到站 (進站間隔 < 10 分鐘)", 8.5, 'BAE6FD', True, 0)], align=PP_ALIGN.CENTER)
    brk_top = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, tl_left + Inches(0.22), r3_top + Inches(0.66), Inches(2.22), Inches(0.015))
    brk_top.fill.solid()
    brk_top.fill.fore_color.rgb = hex_to_rgb('38BDF8')
    brk_top.line.fill.background()

    arr_offsets = [0.22, 0.65, 1.12, 1.34, 1.56, 1.92, 2.34]
    arr_widths  = [0.11, 0.17, 0.11, 0.12, 0.15, 0.15, 0.11]
    for ox, ow in zip(arr_offsets, arr_widths):
        b_arr = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, tl_left + Inches(ox), tl_axis_y - Inches(0.44), Inches(ow), Inches(0.44))
        b_arr.fill.solid()
        b_arr.fill.fore_color.rgb = hex_to_rgb('1E4E68')
        b_arr.line.color.rgb = hex_to_rgb('38BDF8')
        b_arr.line.width = Pt(1.0)

    vac_left = tl_left + Inches(2.68)
    vac_w = Inches(0.88)
    add_text_box(s1, vac_left - Inches(0.18), r3_top + Inches(0.42), Inches(1.75), Inches(0.24), [("2.5 ~ 3.0 小時無車服務真空期", 8.5, 'FCA5A5', True, 0)], align=PP_ALIGN.CENTER)
    vac_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, vac_left, tl_axis_y - Inches(0.48), vac_w, Inches(0.48))
    vac_box.fill.solid()
    vac_box.fill.fore_color.rgb = hex_to_rgb('4A151B')
    vac_box.line.color.rgb = hex_to_rgb('EF4444')
    vac_box.line.width = Pt(1.2)
    vac_box.line.dash_style = MSO_LINE_DASH_STYLE.DASH

    b_post = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, tl_left + Inches(3.68), tl_axis_y - Inches(0.44), Inches(0.20), Inches(0.44))
    b_post.fill.solid()
    b_post.fill.fore_color.rgb = hex_to_rgb('1E4E68')
    b_post.line.color.rgb = hex_to_rgb('38BDF8')
    b_post.line.width = Pt(1.0)

    axis_ln = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, tl_left, tl_axis_y, tl_w, Inches(0.02))
    axis_ln.fill.solid()
    axis_ln.fill.fore_color.rgb = hex_to_rgb('E2E8F0')
    axis_ln.line.fill.background()

    ticks = [(0.0, "0"), (0.95, "6"), (1.95, "12小時"), (3.05, "18"), (4.05, "24")]
    for tx, tlabel in ticks:
        add_text_box(s1, tl_left + Inches(tx) - Inches(0.25), tl_axis_y + Inches(0.03), Inches(0.6), Inches(0.24), [(tlabel, 9.0, 'E2E8F0', True, 0)], align=PP_ALIGN.CENTER)

    # Column 3: Right Module (合規稽核裁決與風險指數)
    c3_left = Inches(9.52)
    c3_w = Inches(3.06)
    add_round_rect(s1, c3_left, col_top, c3_w, col_h, '101C2E', '2B4C6F', 1.2, radius=0.03)
    add_text_box(s1, c3_left + Inches(0.08), col_top + Inches(0.12), c3_w - Inches(0.16), Inches(0.4), [("【合規稽核裁決與風險指數】", 14.0, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    gauge_path = os.path.abspath('scratch/icon_gauge_ring.png')
    gauge_w = Inches(1.92)
    gauge_h = Inches(1.92)
    gauge_left = c3_left + (c3_w - gauge_w) / 2
    gauge_top = col_top + Inches(0.60)
    if os.path.exists(gauge_path):
        s1.shapes.add_picture(gauge_path, gauge_left, gauge_top, gauge_w, gauge_h)

    kpi_pill = add_round_rect(s1, c3_left + Inches(0.16), col_top + Inches(0.56), Inches(0.56), Inches(0.28), '132F4C', '38BDF8', 1.0, radius=0.25)
    add_text_box(s1, c3_left + Inches(0.16), col_top + Inches(0.56), Inches(0.56), Inches(0.28), [("KPI", 9.5, '7DD3FC', True, 0)], align=PP_ALIGN.CENTER)
    add_text_box(s1, gauge_left + Inches(0.26), gauge_top + Inches(0.36), gauge_w - Inches(0.52), Inches(1.22), [("指標得分", 10.5, 'CBD5E1', True, 0), ("48.4", 31.0, 'EF4444', True, 0), ("/ 100", 10.5, 'CBD5E1', True, 0)], align=PP_ALIGN.CENTER)

    verdict_top = col_top + Inches(2.60)
    verdict_h = Inches(0.42)
    add_round_rect(s1, c3_left + Inches(0.14), verdict_top, c3_w - Inches(0.28), verdict_h, '5A1218', 'EF4444', 1.5, radius=0.45)
    add_text_box(s1, c3_left + Inches(0.16), verdict_top, c3_w - Inches(0.32), verdict_h, [("評定：不合格 / 極高營運風險", 11.5, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    warnings_data = ["晶圓在製品嚴重滯留風險", "碼頭多車同時到站排隊", "系統彈性餘裕歸零 (無容錯空間)"]
    w_start_top = col_top + Inches(3.18)
    for idx, w_title in enumerate(warnings_data):
        wy = w_start_top + idx * Inches(0.72)
        add_round_rect(s1, c3_left + Inches(0.14), wy, c3_w - Inches(0.28), Inches(0.62), '2A131D', 'B91C1C', 1.2, radius=0.12)
        tri = s1.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, c3_left + Inches(0.28), wy + Inches(0.17), Inches(0.28), Inches(0.26))
        tri.fill.solid()
        tri.fill.fore_color.rgb = hex_to_rgb('EF4444')
        tri.line.fill.background()
        tri.text_frame.paragraphs[0].text = "!"
        tri.text_frame.paragraphs[0].font.size = Pt(9)
        tri.text_frame.paragraphs[0].font.bold = True
        tri.text_frame.paragraphs[0].font.color.rgb = hex_to_rgb('FFFFFF')
        tri.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        add_text_box(s1, c3_left + Inches(0.62), wy + Inches(0.12), c3_w - Inches(0.80), Inches(0.38), [(w_title, 10.5, 'FCA5A5', True, 0)])


    # =========================================================================
    # SLIDE 2: 系統規格與數學約束模型 (System Specifications & Math Formulation)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    setup_background(s2, prs)
    setup_slide_header(
        s2,
        "半導體廠區物流系統規格與數學約束模型",
        "定義 7 大廠區節點網絡、雙層路網架構、6 大剛性硬約束、2 大品質軟約束與雙目標函數"
    )

    # 3-Column Layout
    # Column 1: 實體網絡環境與雙層路網架構 (Dual-Tier Network)
    s2_c1_w = Inches(3.60)
    add_round_rect(s2, c1_left, col_top, s2_c1_w, col_h, '101C2E', '2B4C6F', 1.2, radius=0.03)
    add_text_box(s2, c1_left + Inches(0.1), col_top + Inches(0.12), s2_c1_w - Inches(0.2), Inches(0.4), [("【實體環境與雙層路網架構】", 14.5, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    # Sub-card 1: Fleet & Nodes
    add_round_rect(s2, c1_left + Inches(0.14), col_top + Inches(0.56), s2_c1_w - Inches(0.28), Inches(1.36), '142338', '38BDF8', 1.0, radius=0.04)
    add_text_box(
        s2, c1_left + Inches(0.22), col_top + Inches(0.62), s2_c1_w - Inches(0.44), Inches(1.24),
        [
            ("7 廠區節點 × 5 部車輛 × 22 條路線", 11.5, '7DD3FC', True, 3),
            ("• 廠區節點：8AB大廳, 8CD碼頭, 8E大廳, 8F代工碼頭, 8S大廳, 嘉晶篤行, 嘉晶創新", 9.5, 'E2E8F0', False, 2),
            ("• 車輛編制：5 部 3.5 噸箱型車 (Car A~E，排除 Car U)，容量 48 批/趟 (4籠×12)", 9.5, 'E2E8F0', False, 2),
            ("• 全網日搬運需求：22 條走廊合計 5,742 批/天，24H 雙班連續運轉 (全日198站次)", 9.5, 'E2E8F0', False, 0)
        ]
    )

    # Sub-card 2: Tier 1 Express Mode
    add_round_rect(s2, c1_left + Inches(0.14), col_top + Inches(2.04), s2_c1_w - Inches(0.28), Inches(1.50), '142338', '10B981', 1.0, radius=0.04)
    add_text_box(
        s2, c1_left + Inches(0.22), col_top + Inches(2.10), s2_c1_w - Inches(0.44), Inches(1.38),
        [
            ("第一層：點對點滿載專車 (Express Tier)", 11.5, '34D399', True, 3),
            ("• 專門服務大宗走廊 (如 8F➔8S 858批, 8AB➔8F 532批, 8CD➔8F 439批 等)", 9.5, 'E2E8F0', False, 2),
            ("• 單趟滿載 48 批，裝卸時間 15 分鐘，直達目的地全數卸除", 9.5, 'E2E8F0', False, 2),
            ("• 全日配置 72 專車站次，提供高達 6,912 批/天之主幹運能", 9.5, 'E2E8F0', False, 0)
        ]
    )

    # Sub-card 3: Tier 2 Rolling Circuit Mode
    add_round_rect(s2, c1_left + Inches(0.14), col_top + Inches(3.66), s2_c1_w - Inches(0.28), Inches(1.56), '142338', 'F59E0B', 1.0, radius=0.04)
    add_text_box(
        s2, c1_left + Inches(0.22), col_top + Inches(3.72), s2_c1_w - Inches(0.44), Inches(1.44),
        [
            ("第二層：歐拉環廠滾動承載 (Rolling Circuit)", 11.5, 'FBBF24', True, 3),
            ("• 兼顧中小批量與跨廠流動需求，遵循滾動承載協議：", 9.5, 'E2E8F0', False, 2),
            ("  - 首站出發：滿載 48 批 (往後第一站36批 + 往後第二站12批)", 9.0, 'CBD5E1', False, 1),
            ("  - 途中各站：上貨 24 批 (各12批)，車上隨時保底留空 ≥24 批空位", 9.0, 'CBD5E1', False, 1),
            ("  - 倒數第二站：解除保留，滿車 48 批直達末站全卸，全日 12 站次", 9.0, 'CBD5E1', False, 0)
        ]
    )

    # Column 2: 六大剛性硬約束 (RULE-HARD-1~6)
    c2_w_s2 = Inches(4.70)
    add_round_rect(s2, c2_left, col_top, c2_w_s2, col_h, '101C2E', '10B981', 1.2, radius=0.025)
    add_text_box(s2, c2_left + Inches(0.15), col_top + Inches(0.12), c2_w_s2 - Inches(0.3), Inches(0.4), [("【六大剛性硬約束 (Hard Constraints 1~6)】", 15, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    h_rules_deck = [
        ("RULE-HARD-1", "車輛容量物理極限", "車輛在任何在途路段之總負載嚴格 ≤ 48 批 (4籠×12儲位)，嚴禁超載。", '10B981'),
        ("RULE-HARD-2", "環廠滾動空間協議", "首站滿載 48 / 途中保底留空 ≥24 / 倒數第二站滿車 48 批直達末站全卸。", '34D399'),
        ("RULE-HARD-3", "22 條走廊頻率保底", "全網 22 條需求走廊每 12 小時班次訪問趟數 N ≥ 1 趟，杜絕跨班斷料。", '38BDF8'),
        ("RULE-HARD-4", "走廊利用率紅線 ≤85%", "各走廊需求/供給利用率全數 ≤ 85.0%，保留 ≥15% 安全抗震緩衝裕度。", '60A5FA'),
        ("RULE-HARD-5", "司機休息與泊位清空", "午晚餐/交接 60 分鐘；外包廠禁休；車輛移至專屬停車區不佔泊位。", 'FBBF24'),
        ("RULE-HARD-6", "物理時間不可壓縮", "廠間通行 (5~15m) 與裝卸作業 (5~15m) 為實體剛性，嚴禁壓縮偷時間。", 'F87171')
    ]
    hr_top = col_top + Inches(0.56)
    for r_code, r_title, r_desc, r_col in h_rules_deck:
        add_round_rect(s2, c2_left + Inches(0.14), hr_top, c2_w_s2 - Inches(0.28), Inches(0.74), '142338', r_col, 1.0, radius=0.04)
        add_text_box(
            s2, c2_left + Inches(0.24), hr_top + Inches(0.06), c2_w_s2 - Inches(0.48), Inches(0.64),
            [
                (f"[{r_code}]  {r_title}", 11, r_col, True, 2),
                (r_desc, 9.5, 'E2E8F0', False, 0)
            ]
        )
        hr_top += Inches(0.78)

    # Column 3: 兩大軟約束與雙目標函數 (Soft Constraints & Objectives)
    c3_left_s2 = c2_left + c2_w_s2 + Inches(0.16)
    c3_w_s2 = Inches(3.32)
    add_round_rect(s2, c3_left_s2, col_top, c3_w_s2, col_h, '101C2E', 'F59E0B', 1.2, radius=0.03)
    add_text_box(s2, c3_left_s2 + Inches(0.08), col_top + Inches(0.12), c3_w_s2 - Inches(0.16), Inches(0.4), [("【軟約束指標與雙目標函數】", 14.0, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    s2_softs = [
        ("RULE-SOFT-1 碼頭進站班距", "同一碼頭任意兩車抵達間隔 ≥ 10 分鐘，消除碼頭排隊與泊位佔用。\n方案三達成 0 衝突 (100.0 分)。", 'FBBF24', '451A03'),
        ("RULE-SOFT-2 出發目的地不重複", "同一廠區連續兩班次開往不同目的地，促進跨廠空間多向分流。\n方案三達成 0 警告 (100.0 分)。", 'FCD34D', '3B2B10'),
        ("目標函數 1：Min Slack (空檔=0)", "最小化車隊全網無效空檔等待時間：\nmin ∑ Slack = 0 分鐘\n消除任何司機怠速浪費，工時利用最大化。", 'A78BFA', '2E1065'),
        ("目標函數 2：Min 加權等候時間", "最小化晶圓在製品需求加權等候：\nmin ∑ (Wait × Demand) / ∑ Demand\n全網平均等候時間降至 44.3~75.7 分鐘。", '818CF8', '1E1B4B')
    ]
    s2_s_top = col_top + Inches(0.56)
    for st_title, st_desc, fg_c, bg_c in s2_softs:
        add_round_rect(s2, c3_left_s2 + Inches(0.12), s2_s_top, c3_w_s2 - Inches(0.24), Inches(1.14), bg_c, fg_c, 1.0, radius=0.04)
        add_text_box(
            s2, c3_left_s2 + Inches(0.20), s2_s_top + Inches(0.08), c3_w_s2 - Inches(0.40), Inches(1.00),
            [(st_title, 11, fg_c, True, 2), (st_desc, 9.5, 'E2E8F0', False, 0)]
        )
        s2_s_top += Inches(1.20)


    # =========================================================================
    # SLIDE 3: 兩階段解耦演算法架構 (Two-Stage Decoupling Architecture)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    setup_background(s3, prs)
    setup_slide_header(
        s3,
        "兩階段解耦演算法：空間拓撲趟數與時序防撞排程求解",
        "化解 10³⁵ 狀態空間爆炸：Stage 1 (MILP 歐拉雙層拓撲) ➔ Stage 2 (CP-SAT 碼頭互斥時序求解)"
    )

    # 3-Column Progressive Flow
    # Col 1: NP-Hard Bottleneck (Why Decouple?)
    s3_c1_w = Inches(3.60)
    add_round_rect(s3, c1_left, col_top, s3_c1_w, col_h, '101C2E', 'EF4444', 1.2, radius=0.03)
    add_text_box(s3, c1_left + Inches(0.1), col_top + Inches(0.12), s3_c1_w - Inches(0.2), Inches(0.4), [("【複雜度瓶頸：為何傳統暴力必敗？】", 14.5, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    why_deck = [
        ("多重 NP-Hard 複合特徵", "本問題同時包含多商品網路流 (MCF)、雙層路網歐拉迴路 (Eulerian Path) 與累積資源時序排程 (Cumulative Scheduling)，端到端決策空間超過 10³⁵ 種狀態，傳統整數規劃直接求解將陷入組合爆炸。"),
        ("人腦經驗與啟發式死鎖", "人工手動微調單一站點時間，即引發下游碼頭跨車連鎖衝突；傳統 GA/遺傳算法難以保證 100% 遵守 6 大剛性硬約束。"),
        ("核心破局策略：兩階段解耦", "將『空間路網趟數分配 (拓撲層)』與『時間軸防撞時序調度 (時序層)』解耦分治，從根本化解維度災難，收斂時間自數小時降至 3~5 秒。")
    ]
    w_top = col_top + Inches(0.56)
    for wt, wd in why_deck:
        add_round_rect(s3, c1_left + Inches(0.14), w_top, s3_c1_w - Inches(0.28), Inches(1.52), '1A1528', 'F43F5E', 1.0, radius=0.04)
        add_text_box(s3, c1_left + Inches(0.22), w_top + Inches(0.08), s3_c1_w - Inches(0.44), Inches(1.36), [(wt, 11, 'FDA4AF', True, 3), (wd, 9.5, 'E2E8F0', False, 0)])
        w_top += Inches(1.60)

    # Col 2: Stage 1 MILP Eulerian Network
    s3_c2_w = Inches(4.30)
    add_round_rect(s3, c2_left, col_top, s3_c2_w, col_h, '101C2E', '38BDF8', 1.2, radius=0.025)
    add_text_box(s3, c2_left + Inches(0.15), col_top + Inches(0.12), s3_c2_w - Inches(0.3), Inches(0.4), [("【階段一：MILP 歐拉雙層路網趟數分配】", 15, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    s1_deck = [
        ("1. 需求下界解析 (Capacity Lower Bound)", "依利用率 ≤85% 剛性要求，計算 22 條走廊單班最低運能：\nC_min(o,d) = ceil( Demand_24h(o,d) / 1.70 )\n精確鎖定每條走廊不可打破之供給門檻。"),
        ("2. 歐拉閉迴路度數守恆 (Eulerian Conservation)", "為確保 5 部車在 12H 班末能無縫返回母港交接，全網各廠區之進出度數必須完全相等：\n∑_u X_{u,v} = ∑_w X_{v,w}  (∀ 廠區 v)"),
        ("3. 雙層路網精確配比 (84 站點分配)", "求解混合整數線性規劃 (MILP)，配置 12 站環廠滾動承載 + 72 站滿載專車 = 84 站載貨站，100% 運能精準投放於 22 條需求走廊，無效空跑歸零。")
    ]
    s1_t = col_top + Inches(0.56)
    for st, sd in s1_deck:
        add_round_rect(s3, c2_left + Inches(0.14), s1_t, s3_c2_w - Inches(0.28), Inches(1.52), '0C2A4A', '0284C7', 1.0, radius=0.04)
        add_text_box(s3, c2_left + Inches(0.22), s1_t + Inches(0.08), s3_c2_w - Inches(0.44), Inches(1.36), [(st, 11, '7DD3FC', True, 3), (sd, 9.5, 'E2E8F0', False, 0)])
        s1_t += Inches(1.60)

    # Col 3: Stage 2 CP-SAT Scheduling & Stage 3 Validator
    s3_c3_left = c2_left + s3_c2_w + Inches(0.16)
    s3_c3_w = Inches(3.72)
    add_round_rect(s3, s3_c3_left, col_top, s3_c3_w, col_h, '101C2E', '10B981', 1.2, radius=0.03)
    add_text_box(s3, s3_c3_left + Inches(0.08), col_top + Inches(0.12), s3_c3_w - Inches(0.16), Inches(0.4), [("【階段二：CP-SAT 碼頭互斥時序求解】", 14.0, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    s2_deck = [
        ("1. Google OR-Tools CP-SAT 區間建模", "建立整數時間變數 IntervalVar(arr, dep, dwell)；為各碼頭設定 AddNoOverlap 約束，強制兩車進站間隔 ≥ 10 分鐘。"),
        ("2. 跨車微創搜尋 (Micro-Jitter Search)", "針對發車時間進行 ±3~5 分鐘微創擾動，利用專車裝卸時間彈性 (Dwell Absorption) 吸收衝突，達成 Slack = 0 分鐘。"),
        ("3. 獨立驗證引擎 (Stage 3 Validator)", "獨立模組 validator.py 以客觀裁判角度逐筆校驗 198 站次時間與容量，生成 audit_report_plan3.html 與 JSON 報告。")
    ]
    s2_t = col_top + Inches(0.56)
    for st, sd in s2_deck:
        add_round_rect(s3, s3_c3_left + Inches(0.12), s2_t, s3_c3_w - Inches(0.24), Inches(1.52), '064E3B', '10B981', 1.0, radius=0.04)
        add_text_box(s3, s3_c3_left + Inches(0.20), s2_t + Inches(0.08), s3_c3_w - Inches(0.40), Inches(1.36), [(st, 11, '6EE7B7', True, 3), (sd, 9.5, 'E2E8F0', False, 0)])
        s2_t += Inches(1.60)


    # =========================================================================
    # SLIDE 4: 方案三落地成果與全景對比 (Plan 3 Breakthrough Results)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    setup_background(s4, prs)
    setup_slide_header(
        s4,
        "方案三落地成果與全景對比：100% 剛性合規與 100 分滿分通過",
        "原基準 (Baseline) vs. 方案二 (CP-SAT雙層重構) vs. 方案三 (100%剛性落地版) 關鍵營運指標躍升對照"
    )

    # 3-Column Layout: Left (Verdict Comparison), Center (4 Core KPI Blocks), Right (Strategic Value)
    s4_c1_w = Inches(3.40)
    add_round_rect(s4, c1_left, col_top, s4_c1_w, col_h, '101C2E', '2B4C6F', 1.2, radius=0.03)
    add_text_box(s4, c1_left + Inches(0.1), col_top + Inches(0.12), s4_c1_w - Inches(0.2), Inches(0.4), [("【三大方案綜合評分與裁決】", 14.5, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    plans_score_cards = [
        ("原基準方案 (Baseline)", "61.1 分 ｜ 🔴 FAILED (未通過)", "4/6 硬約束合規、73 處嚴重違規\n碼頭衝突 8 次、行車壓縮 62 處\n嚴禁正式上線營運", 'EF4444', '3B141E'),
        ("方案二 (CP-SAT 雙層重構)", "97.6 分 ｜ 🟡 WARNING (條件通過)", "6/6 硬約束 100% 合規、0 違規\n碼頭 0 衝突、Slack = 0 分鐘\n存在 4 處連續同向出發提醒", 'F59E0B', '3B2B10'),
        ("方案三 (100% 剛性合規版)", "100.0 分 ｜ 🟢 PASSED (滿分通過)", "6/6 硬約束 100% 合規、0 違規\n碼頭 0 衝突、出發 0 警告\n卓越品質，准予正式營運！", '10B981', '064E3B')
    ]
    psc_top = col_top + Inches(0.56)
    for p_name, p_score, p_desc, fg_c, bg_c in plans_score_cards:
        add_round_rect(s4, c1_left + Inches(0.14), psc_top, s4_c1_w - Inches(0.28), Inches(1.52), bg_c, fg_c, 1.2, radius=0.04)
        add_text_box(
            s4, c1_left + Inches(0.22), psc_top + Inches(0.10), s4_c1_w - Inches(0.44), Inches(1.36),
            [
                (p_name, 11, 'FFFFFF', True, 2),
                (p_score, 12.5, fg_c, True, 3),
                (p_desc, 9.5, 'E2E8F0', False, 0)
            ]
        )
        psc_top += Inches(1.60)

    # Center Column: 4 KPI Cards (2x2 Grid) + Visual Bar Chart
    s4_c2_left = c1_left + s4_c1_w + Inches(0.18)
    s4_c2_w = Inches(5.10)
    add_round_rect(s4, s4_c2_left, col_top, s4_c2_w, col_h, '101C2E', '10B981', 1.2, radius=0.025)
    add_text_box(s4, s4_c2_left + Inches(0.15), col_top + Inches(0.12), s4_c2_w - Inches(0.3), Inches(0.4), [("【方案三關鍵營運指標 (KPI) 突破成果】", 15, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    s4_kpis = [
        ("全網有效總運能", "7,776 批/天", "原基準 6,000 批 ➔ 擴增 +29.6%", '34D399', '064E3B'),
        ("走廊最高利用率", "84.7%", "原基準 200.0% ➔ 全數 ≤85.0%", '38BDF8', '0C4A6E'),
        ("碼頭進站衝突數", "0 件 (歸零)", "班距 100% ≥10 分鐘 (原 8 件)", 'FBBF24', '451A03'),
        ("全網無效等待 (Slack)", "0 分鐘/日", "消除全部浪費 (原 60 分鐘)", 'A78BFA', '2E1065')
    ]
    s4_g_top = col_top + Inches(0.56)
    c_w_s4 = Inches(2.35)
    c_h_s4 = Inches(1.50)
    for idx, (kn, kv, ks, fgc, bgc) in enumerate(s4_kpis):
        gx = s4_c2_left + Inches(0.14) if idx % 2 == 0 else s4_c2_left + Inches(2.61)
        gy = s4_g_top if idx < 2 else s4_g_top + Inches(1.58)
        add_round_rect(s4, gx, gy, c_w_s4, c_h_s4, bgc, fgc, 1.2, radius=0.06)
        add_text_box(
            s4, gx + Inches(0.10), gy + Inches(0.12), c_w_s4 - Inches(0.20), c_h_s4 - Inches(0.20),
            [(kn, 11, 'FFFFFF', True, 3), (kv, 20, fgc, True, 3), (ks, 9.5, 'E2E8F0', False, 0)],
            align=PP_ALIGN.CENTER
        )

    # Driver & Dock Rule Banner (Bottom of Center)
    s4_bot_top = s4_g_top + Inches(3.22)
    s4_bot_h = col_h - Inches(3.35)
    add_round_rect(s4, s4_c2_left + Inches(0.14), s4_bot_top, s4_c2_w - Inches(0.28), s4_bot_h, '132338', '3B82F6', 1.0, radius=0.04)
    add_text_box(
        s4, s4_c2_left + Inches(0.25), s4_bot_top + Inches(0.10), s4_c2_w - Inches(0.5), s4_bot_h - Inches(0.2),
        [
            ("司機休息合規與碼頭泊位清空管理落實：", 11.5, '93C5FD', True, 3),
            ("• 60 分鐘午晚餐/交接足額保障，全面杜絕疲勞駕駛與超速趕工工安風險。", 10, 'E2E8F0', False, 2),
            ("• 休息時車輛必須移至本廠專屬停車區或休息室旁，絕不佔據碼頭作業泊位。", 10, 'E2E8F0', False, 2),
            ("• 嚴格禁止於外包廠（嘉晶）休息，100% 符合半導體代工資安與廠規管理標準。", 10, 'E2E8F0', False, 0)
        ]
    )

    # Right Column: 戰略價值與管理決策
    s4_c3_left = s4_c2_left + s4_c2_w + Inches(0.18)
    s4_c3_w = Inches(3.12)
    add_round_rect(s4, s4_c3_left, col_top, s4_c3_w, col_h, '101C2E', 'F59E0B', 1.2, radius=0.03)
    add_text_box(s4, s4_c3_left + Inches(0.15), col_top + Inches(0.12), s4_c3_w - Inches(0.3), Inches(0.4), [("【戰略價值與管理決策】", 13.5, 'FFFFFF', True, 0)], align=PP_ALIGN.CENTER)

    s4_strat = [
        ("零資本支出 (CAPEX = $0)", "常態維持 5 部車隊（排除 Car U），完全無需購置新車或額外增聘司機，效益最大化。", '10B981', '064E3B'),
        ("安全抗震裕度 ≥ 15%", "22 條走廊利用率全數 ≤85.0%，足以吸收每日產線急件、機台回補與異常波動。", '38BDF8', '0C4A6E'),
        ("建議立即核准正式上線", "方案三各項硬約束 100% 合規、軟約束 100 分，建議運籌生管部門立即啟動新表切換。", 'FBBF24', '451A03'),
        ("日常維護：Excel 動態重算", "生管需求變動時，於戰情室拖曳上傳 Demand_from_to.xlsx，5 秒完成自動重新排程。", 'A78BFA', '2E1065')
    ]
    s4_st_top = col_top + Inches(0.56)
    for st_t, st_d, fg_c, bg_c in s4_strat:
        add_round_rect(s4, s4_c3_left + Inches(0.12), s4_st_top, s4_c3_w - Inches(0.24), Inches(1.14), bg_c, fg_c, 1.0, radius=0.04)
        add_text_box(
            s4, s4_c3_left + Inches(0.20), s4_st_top + Inches(0.08), s4_c3_w - Inches(0.40), Inches(1.00),
            [(st_t, 11, fg_c, True, 2), (st_d, 9.5, 'E2E8F0', False, 0)]
        )
        s4_st_top += Inches(1.20)


    # =========================================================================
    # SLIDE 5: AI 工具鏈端到端解題實踐 (AI-Assisted Methodology & Engineering)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    setup_background(s5, prs)
    setup_slide_header(
        s5,
        "如何利用 Antigravity AI 工具鏈端到端解決複雜物流難題",
        "演算法選型、數學建模、生產級程式碼落地、自動化審查與動態 Excel 重算管線研發"
    )

    # 4 Columns Modern Architecture (2.85 in each)
    p_w = Inches(2.85)
    p_gap = Inches(0.18)
    p_left_base = Inches(0.75)

    s5_pillars = [
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

    for idx, (p_title, p_sub, p_body, fg_c, bg_c) in enumerate(s5_pillars):
        px = p_left_base + idx * (p_w + p_gap)
        add_round_rect(s5, px, col_top, p_w, col_h, '101C2E', fg_c, 1.2, radius=0.03)
        add_round_rect(s5, px + Inches(0.10), col_top + Inches(0.12), p_w - Inches(0.20), Inches(0.72), bg_c, fg_c, 1.0, radius=0.04)
        add_text_box(s5, px + Inches(0.14), col_top + Inches(0.16), p_w - Inches(0.28), Inches(0.64), [(p_title, 11.5, 'FFFFFF', True, 2), (p_sub, 8.5, fg_c, True, 0)], align=PP_ALIGN.CENTER)
        add_round_rect(s5, px + Inches(0.10), col_top + Inches(0.92), p_w - Inches(0.20), col_h - Inches(1.04), '142338', '2B4C6F', 1.0, radius=0.03)
        add_text_box(s5, px + Inches(0.18), col_top + Inches(1.04), p_w - Inches(0.36), col_h - Inches(1.24), [(p_body, 10, 'E2E8F0', False, 0)])

    prs.save(output_path)
    print(f"--> 全圖表 5 頁完整簡報成功儲存至：{output_path}")


if __name__ == '__main__':
    out_name = '半導體廠區物流排程優化_高階主管報告與演算法規格.pptx'
    build_full_deck(out_name)
    print("生成完畢！")
