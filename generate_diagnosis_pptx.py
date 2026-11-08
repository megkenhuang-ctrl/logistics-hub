# -*- coding: utf-8 -*-
import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE


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


def create_presentation():
    prs = Presentation()
    # Standard 16:9 Widescreen (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: 100% NATIVE EDITABLE EXECUTIVE INFOGRAPHIC SLIDE
    # =========================================================================
    slide = prs.slides.add_slide(blank_layout)

    # 0. Dark-Tech Circuit Board Background (clean without any baked-in text)
    bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_rect.fill.solid()
    bg_rect.fill.fore_color.rgb = hex_to_rgb('070F1C')
    bg_rect.line.fill.background()

    bg_clean_path = os.path.abspath('scratch/ppt_bg_clean.png')
    if os.path.exists(bg_clean_path):
        slide.shapes.add_picture(bg_clean_path, Inches(0.35), Inches(0.25), Inches(12.633), Inches(7.0))

    # 1. Top Title & Subtitle (Independent Editable Text Boxes, no bulky border box)
    add_text_box(
        slide,
        Inches(1.5), Inches(0.42), Inches(10.333), Inches(0.65),
        [("跨廠物流營運現況診斷與痛點分析", 29, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )
    add_text_box(
        slide,
        Inches(1.5), Inches(1.06), Inches(10.333), Inches(0.42),
        [("半導體多廠區物料轉運與車輛排程瓶頸結構性解構", 15.5, '7DD3FC', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # Common column vertical dimensions
    col_top = Inches(1.65)
    col_h = Inches(5.38)

    # =========================================================================
    # COLUMN 1: LEFT MODULE (【核心根因：人工排程瓶頸】)
    # =========================================================================
    c1_left = Inches(0.75)
    c1_w = Inches(3.38)

    # Top Group Card (Root Cause + Brain->Chip + Variables)
    c1_top_h = Inches(3.85)
    add_round_rect(slide, c1_left, col_top, c1_w, c1_top_h, '101C2E', '2B4C6F', 1.2, radius=0.03)

    # Column 1 Title
    add_text_box(
        slide,
        c1_left + Inches(0.1), col_top + Inches(0.12), c1_w - Inches(0.2), Inches(0.4),
        [("【核心根因：人工排程瓶頸】", 14.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # Glowing Brain-to-Chip Visual
    brain_chip_path = os.path.abspath('scratch/icon_brain_chip.png')
    if os.path.exists(brain_chip_path):
        slide.shapes.add_picture(
            brain_chip_path,
            c1_left + Inches(0.16), col_top + Inches(0.58),
            c1_w - Inches(0.32), Inches(1.38)
        )

    # Editable Labels under Brain and Chip
    add_text_box(
        slide,
        c1_left + Inches(0.14), col_top + Inches(2.02), Inches(1.45), Inches(0.52),
        [
            ("人腦線性經驗", 11.5, 'FFFFFF', True, 1),
            ("片斷直覺手動調度", 9.5, '94A3B8', False, 0)
        ],
        align=PP_ALIGN.CENTER
    )
    add_text_box(
        slide,
        c1_left + c1_w - Inches(1.68), col_top + Inches(2.02), Inches(1.55), Inches(0.52),
        [
            ("半導體物流網路", 11.5, '7DD3FC', True, 1),
            ("高維時空全局約束", 9.5, '38BDF8', False, 0)
        ],
        align=PP_ALIGN.CENTER
    )

    # High-Dim Variables Pill Box
    var_top = col_top + Inches(2.65)
    var_h = Inches(1.02)
    add_round_rect(
        slide,
        c1_left + Inches(0.16), var_top, c1_w - Inches(0.32), var_h,
        '13253C', '386690', 1.0, radius=0.08
    )
    add_text_box(
        slide,
        c1_left + Inches(0.22), var_top + Inches(0.12), c1_w - Inches(0.44), var_h - Inches(0.2),
        [
            ("5 部專用貨車 × 22 條跨廠路線", 12, 'FFFFFF', True, 6),
            ("198 處停靠站點 × 碼頭泊位限制", 11.5, 'E2E8F0', True, 0)
        ],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # Bottom Golden Key Insight Card
    ins_top = col_top + c1_top_h + Inches(0.15)
    ins_h = col_h - c1_top_h - Inches(0.15)
    add_round_rect(slide, c1_left, ins_top, c1_w, ins_h, '3B2B10', 'D97706', 1.5, radius=0.04)
    # Subtle inner top highlight bar
    add_text_box(
        slide,
        c1_left + Inches(0.15), ins_top + Inches(0.12), c1_w - Inches(0.3), ins_h - Inches(0.2),
        [
            ("【關鍵洞察】", 13.5, 'FBBF24', True, 6),
            ("高維度時空變數組合爆炸，超越人腦認知極限；單一車次微調即引發連鎖排隊，導致被動應付式調度。", 10.5, 'FDE68A', True, 0)
        ],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # =========================================================================
    # COLUMN 2: MIDDLE MODULE (【三大關鍵營運痛點分析】 - 3 Horizontal Rows)
    # =========================================================================
    c2_left = Inches(4.30)
    c2_w = Inches(5.05)

    add_round_rect(slide, c2_left, col_top, c2_w, col_h, '101C2E', '2B4C6F', 1.2, radius=0.025)

    # Column 2 Title
    add_text_box(
        slide,
        c2_left + Inches(0.15), col_top + Inches(0.12), c2_w - Inches(0.3), Inches(0.4),
        [("【三大關鍵營運痛點分析】", 15, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    row_left = c2_left + Inches(0.14)
    row_w = c2_w - Inches(0.28)

    # -------------------------------------------------------------------------
    # ROW 1: 痛點一：18 條路線負荷過載
    # -------------------------------------------------------------------------
    r1_top = col_top + Inches(0.56)
    r1_h = Inches(1.48)
    add_round_rect(slide, row_left, r1_top, row_w, r1_h, '142338', '2C4A6E', 1.0, radius=0.04)

    add_text_box(
        slide,
        row_left + Inches(0.12), r1_top + Inches(0.08), Inches(3.2), Inches(0.32),
        [("痛點一：18 條路線負荷過載", 12.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.LEFT
    )

    # 14 Native Vector Bars (Left half of Row 1)
    chart_base_y = r1_top + Inches(1.32)
    chart_left_x = row_left + Inches(0.18)
    bar_heights_in = [0.24, 0.30, 0.35, 0.32, 0.50, 0.72, 0.32, 0.25, 0.38, 0.44, 0.44, 0.36, 0.42, 0.80]
    bar_w_in = 0.115
    bar_step_in = 0.165

    for idx, bh in enumerate(bar_heights_in):
        bx = chart_left_x + Inches(idx * bar_step_in)
        by = chart_base_y - Inches(bh)
        b_col = 'EF4444' if idx == 13 else '38BDF8'
        bar_sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, by, Inches(bar_w_in), Inches(bh))
        bar_sh.fill.solid()
        bar_sh.fill.fore_color.rgb = hex_to_rgb(b_col)
        bar_sh.line.fill.background()

    # Baseline under bars
    base_ln = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        chart_left_x - Inches(0.04), chart_base_y, Inches(2.38), Inches(0.015)
    )
    base_ln.fill.solid()
    base_ln.fill.fore_color.rgb = hex_to_rgb('94A3B8')
    base_ln.line.fill.background()

    # 85% Red Dashed Safety Threshold Line
    thresh_y = chart_base_y - Inches(0.60)
    for dash_i in range(18):
        dx = chart_left_x - Inches(0.02) + Inches(dash_i * 0.13)
        d_seg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, dx, thresh_y, Inches(0.075), Inches(0.018))
        d_seg.fill.solid()
        d_seg.fill.fore_color.rgb = hex_to_rgb('EF4444')
        d_seg.line.fill.background()

    # "85% 安全警戒線" Label & "200%" Label
    add_text_box(
        slide,
        chart_left_x + Inches(0.92), thresh_y - Inches(0.23), Inches(1.25), Inches(0.22),
        [("85% 安全警戒線", 8.5, 'F87171', True, 0)],
        align=PP_ALIGN.RIGHT
    )
    add_text_box(
        slide,
        chart_left_x + Inches(13 * bar_step_in) - Inches(0.14), chart_base_y - Inches(1.02), Inches(0.45), Inches(0.22),
        [("200%", 9.0, 'EF4444', True, 0)],
        align=PP_ALIGN.CENTER
    )

    # Right Description in Row 1
    add_text_box(
        slide,
        row_left + Inches(2.68), r1_top + Inches(0.40), row_w - Inches(2.78), Inches(0.95),
        [
            ("嘉晶外包廠路線負荷達", 11, 'FFFFFF', True, 2),
            ("200%（天天欠料斷線", 11, 'FCA5A5', True, 2),
            ("，物料跨班滯留）", 11, 'FFFFFF', True, 0)
        ],
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE
    )

    # -------------------------------------------------------------------------
    # ROW 2: 痛點二：運輸模式配置僵化
    # -------------------------------------------------------------------------
    r2_top = r1_top + r1_h + Inches(0.12)
    r2_h = Inches(1.48)
    add_round_rect(slide, row_left, r2_top, row_w, r2_h, '142338', '2C4A6E', 1.0, radius=0.04)

    add_text_box(
        slide,
        row_left + Inches(0.12), r2_top + Inches(0.08), Inches(3.2), Inches(0.32),
        [("痛點二：運輸模式配置僵化", 12.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.LEFT
    )

    # Loop-Truck-Lock Graphic on Left of Row 2
    loop_truck_path = os.path.abspath('scratch/icon_loop_truck.png')
    if os.path.exists(loop_truck_path):
        slide.shapes.add_picture(
            loop_truck_path,
            row_left + Inches(0.18), r2_top + Inches(0.36),
            Inches(2.35), Inches(1.02)
        )

    # Right Description in Row 2
    add_text_box(
        slide,
        row_left + Inches(2.68), r2_top + Inches(0.38), row_w - Inches(2.78), Inches(0.98),
        [
            ("全日 0 趟直達專車；48", 11, 'FFFFFF', True, 2),
            ("儲位貨車長期低乘載率", 11, 'FDE68A', True, 2),
            ("，運能嚴重浪費。", 11, 'FFFFFF', True, 0)
        ],
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE
    )

    # -------------------------------------------------------------------------
    # ROW 3: 痛點三：多車同時到站與服務真空
    # -------------------------------------------------------------------------
    r3_top = r2_top + r2_h + Inches(0.12)
    r3_h = Inches(1.56)
    add_round_rect(slide, row_left, r3_top, row_w, r3_h, '142338', '2C4A6E', 1.0, radius=0.04)

    add_text_box(
        slide,
        row_left + Inches(0.12), r3_top + Inches(0.08), Inches(2.65), Inches(0.32),
        [("痛點三：多車同時到站與服務真空", 11.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.LEFT
    )

    # Top-Right Pill Badge: 晶圓在製品平均等候時間：131.6 分鐘
    wip_pill = add_round_rect(
        slide,
        row_left + Inches(2.70), r3_top + Inches(0.07), row_w - Inches(2.80), Inches(0.28),
        '1A2A40', '475569', 1.0, radius=0.25
    )
    add_text_box(
        slide,
        row_left + Inches(2.71), r3_top + Inches(0.07), row_w - Inches(2.82), Inches(0.28),
        [("晶圓在製品平均等候時間：131.6 分鐘", 7.8, 'FBBF24', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # Timeline Graphic inside Row 3
    tl_left = row_left + Inches(0.22)
    tl_w = row_w - Inches(0.48)
    tl_axis_y = r3_top + Inches(1.22)

    # Top label for Simultaneous Arrivals + Bracket
    add_text_box(
        slide,
        tl_left - Inches(0.05), r3_top + Inches(0.42), Inches(2.52), Inches(0.24),
        [("8 次碼頭同時到站 (進站間隔 < 10 分鐘)", 8.5, 'BAE6FD', True, 0)],
        align=PP_ALIGN.CENTER
    )
    # Horizontal bracket line over the 6 arrival bars
    brk_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, tl_left + Inches(0.22), r3_top + Inches(0.66), Inches(2.22), Inches(0.015))
    brk_top.fill.solid()
    brk_top.fill.fore_color.rgb = hex_to_rgb('38BDF8')
    brk_top.line.fill.background()

    # 6 Cyan Arrival Bars along Timeline
    arr_offsets = [0.22, 0.65, 1.12, 1.34, 1.56, 1.92, 2.34]
    arr_widths  = [0.11, 0.17, 0.11, 0.12, 0.15, 0.15, 0.11]
    for ox, ow in zip(arr_offsets, arr_widths):
        b_arr = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            tl_left + Inches(ox), tl_axis_y - Inches(0.44), Inches(ow), Inches(0.44)
        )
        b_arr.fill.solid()
        b_arr.fill.fore_color.rgb = hex_to_rgb('1E4E68')
        b_arr.line.color.rgb = hex_to_rgb('38BDF8')
        b_arr.line.width = Pt(1.0)

    # Red Service Vacuum Block (2.5 ~ 3.0 小時無車服務真空期)
    vac_left = tl_left + Inches(2.68)
    vac_w = Inches(0.88)
    add_text_box(
        slide,
        vac_left - Inches(0.18), r3_top + Inches(0.42), Inches(1.75), Inches(0.24),
        [("2.5 ~ 3.0 小時無車服務真空期", 8.5, 'FCA5A5', True, 0)],
        align=PP_ALIGN.CENTER
    )
    vac_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        vac_left, tl_axis_y - Inches(0.48), vac_w, Inches(0.48)
    )
    vac_box.fill.solid()
    vac_box.fill.fore_color.rgb = hex_to_rgb('4A151B')
    vac_box.line.color.rgb = hex_to_rgb('EF4444')
    vac_box.line.width = Pt(1.2)
    vac_box.line.dash_style = MSO_LINE_DASH_STYLE.DASH

    # Post-vacuum bar
    b_post = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        tl_left + Inches(3.68), tl_axis_y - Inches(0.44), Inches(0.20), Inches(0.44)
    )
    b_post.fill.solid()
    b_post.fill.fore_color.rgb = hex_to_rgb('1E4E68')
    b_post.line.color.rgb = hex_to_rgb('38BDF8')
    b_post.line.width = Pt(1.0)

    # Timeline Horizontal Axis Line
    axis_ln = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        tl_left, tl_axis_y, tl_w, Inches(0.02)
    )
    axis_ln.fill.solid()
    axis_ln.fill.fore_color.rgb = hex_to_rgb('E2E8F0')
    axis_ln.line.fill.background()

    # Timeline Tick Labels (0, 6, 12小時, 18, 24)
    ticks = [
        (0.0, "0"),
        (0.95, "6"),
        (1.95, "12小時"),
        (3.05, "18"),
        (4.05, "24")
    ]
    for tx, tlabel in ticks:
        add_text_box(
            slide,
            tl_left + Inches(tx) - Inches(0.25), tl_axis_y + Inches(0.03), Inches(0.6), Inches(0.24),
            [(tlabel, 9.0, 'E2E8F0', True, 0)],
            align=PP_ALIGN.CENTER
        )

    # =========================================================================
    # COLUMN 3: RIGHT MODULE (【合規稽核裁決與風險指數】)
    # =========================================================================
    c3_left = Inches(9.52)
    c3_w = Inches(3.06)

    add_round_rect(slide, c3_left, col_top, c3_w, col_h, '101C2E', '2B4C6F', 1.2, radius=0.03)

    # Column 3 Title
    add_text_box(
        slide,
        c3_left + Inches(0.08), col_top + Inches(0.12), c3_w - Inches(0.16), Inches(0.4),
        [("【合規稽核裁決與風險指數】", 14.0, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # Glowing Red Multi-Ring Gauge Image + Editable Center Score Text Box
    gauge_path = os.path.abspath('scratch/icon_gauge_ring.png')
    gauge_w = Inches(1.92)
    gauge_h = Inches(1.92)
    gauge_left = c3_left + (c3_w - gauge_w) / 2
    gauge_top = col_top + Inches(0.60)
    if os.path.exists(gauge_path):
        slide.shapes.add_picture(gauge_path, gauge_left, gauge_top, gauge_w, gauge_h)

    # KPI Badge (Top-Left of Column 3, layered above gauge corner)
    kpi_pill = add_round_rect(
        slide,
        c3_left + Inches(0.16), col_top + Inches(0.56), Inches(0.56), Inches(0.28),
        '132F4C', '38BDF8', 1.0, radius=0.25
    )
    add_text_box(
        slide,
        c3_left + Inches(0.16), col_top + Inches(0.56), Inches(0.56), Inches(0.28),
        [("KPI", 9.5, '7DD3FC', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # Native Editable Text Box right in the center of the Gauge Ring
    add_text_box(
        slide,
        gauge_left + Inches(0.26), gauge_top + Inches(0.36), gauge_w - Inches(0.52), Inches(1.22),
        [
            ("指標得分", 10.5, 'CBD5E1', True, 0),
            ("48.4", 31.0, 'EF4444', True, 0),
            ("/ 100", 10.5, 'CBD5E1', True, 0)
        ],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # Verdict Pill Button: 評定：不合格 / 極高營運風險
    verdict_top = col_top + Inches(2.60)
    verdict_h = Inches(0.42)
    add_round_rect(
        slide,
        c3_left + Inches(0.14), verdict_top, c3_w - Inches(0.28), verdict_h,
        '5A1218', 'EF4444', 1.5, radius=0.45
    )
    add_text_box(
        slide,
        c3_left + Inches(0.16), verdict_top, c3_w - Inches(0.32), verdict_h,
        [("評定：不合格 / 極高營運風險", 11.5, 'FFFFFF', True, 0)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    # 3 Sleek Individual Warning Cards at the bottom of Column 3
    warnings_data = [
        "晶圓在製品嚴重滯留風險",
        "碼頭多車同時到站排隊",
        "系統彈性餘裕歸零 (無容錯空間)"
    ]
    w_start_top = col_top + Inches(3.18)
    w_card_h = Inches(0.62)
    w_gap = Inches(0.10)

    for idx, w_title in enumerate(warnings_data):
        wy = w_start_top + idx * (w_card_h + w_gap)
        add_round_rect(
            slide,
            c3_left + Inches(0.14), wy, c3_w - Inches(0.28), w_card_h,
            '2A131D', 'B91C1C', 1.2, radius=0.12
        )
        # Red Triangle Warning Icon (Native Vector Shape)
        tri = slide.shapes.add_shape(
            MSO_SHAPE.ISOSCELES_TRIANGLE,
            c3_left + Inches(0.28), wy + Inches(0.17), Inches(0.28), Inches(0.26)
        )
        tri.fill.solid()
        tri.fill.fore_color.rgb = hex_to_rgb('EF4444')
        tri.line.fill.background()
        tf_t = tri.text_frame
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = "!"
        p_t.font.name = "Arial"
        p_t.font.size = Pt(9)
        p_t.font.bold = True
        p_t.font.color.rgb = hex_to_rgb('FFFFFF')
        p_t.alignment = PP_ALIGN.CENTER

        # Editable Warning Text Box
        add_text_box(
            slide,
            c3_left + Inches(0.64), wy + Inches(0.06), c3_w - Inches(0.84), w_card_h - Inches(0.12),
            [(w_title, 11.0, 'FFFFFF', True, 0)],
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE
        )

    # =========================================================================
    # SLIDE 2: AI HIGH-RES VISUAL REFERENCE SLIDE (視覺原圖對照)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    bg2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg2.fill.solid()
    bg2.fill.fore_color.rgb = hex_to_rgb('070F1C')
    bg2.line.fill.background()

    img_path = os.path.abspath('scratch/executive_ai_infographic.jpg')
    if os.path.exists(img_path):
        slide2.shapes.add_picture(img_path, Inches(0.5), Inches(0.4), Inches(12.333), Inches(6.7))

    # Save to scratch & all target files
    out_scratch = os.path.abspath('scratch/executive_diagnosis_editable.pptx')
    prs.save(out_scratch)

    target_files = [
        '現況診斷與運籌痛點分析.pptx',
        '現況診斷與運籌痛點分析_可編輯簡報.pptx',
        '現況診斷與關鍵營運痛點分析.pptx'
    ]
    for tf_name in target_files:
        tf_path = os.path.abspath(tf_name)
        try:
            shutil.copyfile(out_scratch, tf_path)
            print(f"Saved: {tf_path}")
        except PermissionError:
            print(f"File currently open in PowerPoint, will close via COM and update: {tf_path}")

    return out_scratch


if __name__ == '__main__':
    create_presentation()
