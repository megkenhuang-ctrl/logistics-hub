import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Tech Palette
    DARK_BLUE = RGBColor(15, 32, 67)      # #0F2043 (Deep Tech Navy)
    PRIMARY_BLUE = RGBColor(24, 76, 120)  # #184C78 (Slate Blue)
    ACCENT_BLUE = RGBColor(0, 114, 206)   # #0072CE (Vibrant Blue)
    LIGHT_BG = RGBColor(248, 250, 252)    # #F8FAFC (Clean Light Grey)
    WHITE = RGBColor(255, 255, 255)
    DARK_TEXT = RGBColor(30, 41, 59)      # #1E293B (Dark Slate)
    MUTED_TEXT = RGBColor(100, 116, 139)  # #64748B
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    HIGHLIGHT_ORANGE = RGBColor(234, 88, 12) # #EA580C
    HIGHLIGHT_GREEN = RGBColor(16, 149, 113) # #10B981

    FONT_MAIN = "Microsoft JhengHei"
    FONT_ENG = "Segoe UI"

    def add_header(slide, title_text, category_text="LOGISTICS OPERATIONS RESEARCH"):
        # Category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_ENG
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.7))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = FONT_MAIN
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = DARK_BLUE

    def create_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    # =========================================================================
    # SLIDE 1: 資源盤點與系統基本面 (Resources & Baseline)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_header(s1, "01 | 資源盤點與系統基本面：5 部車、6 節點與 24H 連續運轉", "RESOURCES & PHYSICAL NETWORK")

    # 3 Summary Cards across top
    cards_data = [
        ("移動載具資源", "5 部常態作業貨車", "Car A、B、C、D、E\n每車物理極限 40 批/趟\n五大母港清晨分散首發", PRIMARY_BLUE),
        ("作業時間制度", "24H 雙班完全鏡像", "日班：07:35 ~ 19:35 (12H)\n夜班：19:35 ~ 07:35 (12H)\n扣除用餐/交接，淨工時 600m", ACCENT_BLUE),
        ("空間網絡節點", "6 大實體作業站點", "力行核心：8AB(大廳), 8CD(碼頭3F)\n外圍廠區：8E(大廳), 8F(代工), 8S(庫房)\n長途外廠：嘉晶 (創新/篤行)", DARK_BLUE)
    ]
    for i, (title, sub, body, color) in enumerate(cards_data):
        c_left = Inches(0.8 + i * 4.0)
        c = create_card(s1, c_left, Inches(1.6), Inches(3.7), Inches(2.2))
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.18)
        tf.margin_left = tf.margin_right = Inches(0.2)
        
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = color
        
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = DARK_TEXT
        p2.space_before = Pt(4)
        p2.space_after = Pt(8)
        
        p3 = tf.add_paragraph()
        p3.text = body
        p3.font.name = FONT_MAIN
        p3.font.size = Pt(11)
        p3.font.color.rgb = MUTED_TEXT

    # Lower Table: 6 Nodes Characteristics
    t_shape = s1.shapes.add_table(7, 4, Inches(0.8), Inches(4.1), Inches(11.7), Inches(2.8))
    table = t_shape.table
    table.columns[0].width = Inches(2.0)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(4.5)
    table.columns[3].width = Inches(3.0)

    headers = ["廠區站點", "具體作業位置", "實體搬運動線與工時特性", "駐點母車 / 角色定位"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_MAIN
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    node_rows = [
        ("FAB8CD", "裝卸碼頭上 3F 換車", "碼頭卸貨 ➔ 搭貨梯上 3 樓 ➔ 換車點交 (工時 20~25m)", "Car D 母港 ｜ 力行物料集散大港"),
        ("FAB8F", "代工出入口上 3F 換車", "全廠最大十字路口，代工口卸貨 ➔ 搭梯上 3F 換車 (25m)", "Car B 母港 ｜ 全廠第 1 大發車熱點 (42趟)"),
        ("FAB8AB", "1F 大廳 (平面作業)", "大廳純平面換貨，人員直接現場清點，無電梯等待 (20m)", "Car C 母港 ｜ 力行製造核心動脈"),
        ("FAB8E", "1F 大廳 (平面交接)", "外圍廠區重要門戶，大廳換車與平面點交 (20~25m)", "Car A 母港 ｜ 外圍大廳高頻樞紐"),
        ("FAB8S", "1F 碼頭長推至 8S5A", "非最大集散地，1F 碼頭長距離跋涉推至 8S5A 庫房 (40~55m)", "Car E 母港 ｜ 總庫房重物料發貨港"),
        ("嘉晶 (創新/篤行)", "外廠警衛室/碼頭", "外廠門口快收快送，晶圓代工與加工片接駁 (10~20m)", "Car A 專營 ｜ 定時長途外廠專線")
    ]
    for row_idx, r_data in enumerate(node_rows, start=1):
        for col_idx, text in enumerate(r_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_MAIN
            p.font.size = Pt(10)
            p.font.color.rgb = DARK_TEXT
            if col_idx in [0, 1]:
                p.font.bold = True
                p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: 車輛任務與營運模式分流 (The Mission)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "02 | 車輛任務與貨流分流：主動脈專車 (65%) ＋ 毛細管環廠 (35%)", "THE DUAL-MODE OPERATIONAL MATRIX")

    # 2 Big Mode Cards
    modes = [
        ("專車模式 (Point-to-Point Trunkline)", 
         "極致單次大吞吐量", 
         PRIMARY_BLUE,
         [("適用對象", "集中型大單、主幹動脈 (單批需求 > 24 批)"),
          ("裝載規則", "車廂 100% 塞滿至 40 批物理極限 (滿進滿出)"),
          ("核心航段", "8F ↔ 8CD、8AB ↔ 8F、8S ↔ 8CD、8CD ↔ 8AB"),
          ("承運主力", "Car B (13趟)、Car C (9趟)、Car E (9趟)"),
          ("營運佔比", "貢獻全車隊約 65% ~ 70% 總有效運能")]),

        ("環廠巡迴模式 (Milk-Run / Pipeline)", 
         "極致連通度與高頻率", 
         ACCENT_BLUE,
         [("適用對象", "零散料、尾數箱、樣品、治具、跨廠多點互轉 (≤ 16 批)"),
          ("裝載規則", "嚴守『16/24 動態紅線』，車廂隨時留 24 批空位給下站"),
          ("核心航段", "全日大外圈 (Car D)、下午外圍小環 (Car B / C / E)"),
          ("承運主力", "Car D (全日純環廠 16航段)、Car A (外廠大環)"),
          ("營運佔比", "貢獻全車隊約 30% ~ 35% 運能，消滅全廠拒載")])
    ]

    for i, (m_title, m_tag, m_col, items) in enumerate(modes):
        c_left = Inches(0.8 + i * 5.9)
        card = create_card(s2, c_left, Inches(1.6), Inches(5.8), Inches(5.3))
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.2)
        tf.margin_left = tf.margin_right = Inches(0.25)
        
        p1 = tf.paragraphs[0]
        p1.text = m_title
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = m_col
        
        p2 = tf.add_paragraph()
        p2.text = f"● 目標導向：{m_tag}"
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = DARK_TEXT
        p2.space_before = Pt(4)
        p2.space_after = Pt(12)

        for label, val in items:
            p_item = tf.add_paragraph()
            p_item.text = f"▪ {label}：{val}"
            p_item.font.name = FONT_MAIN
            p_item.font.size = Pt(11)
            p_item.font.color.rgb = DARK_TEXT
            p_item.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: 現場硬約束與瓶頸分析 (The Real Constraints)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "03 | 現場三大硬約束與瓶頸：時間、動線與環廠死鎖矛盾", "PHYSICAL & OPERATIONAL CONSTRAINTS")

    constraints = [
        ("① 時間硬約束：淨作業時間僅 600m", 
         "單班 720 分鐘 (12H) 法定扣除：\n▪ 同仁用餐：60 分鐘 (鎖車不跑單)\n▪ 班末交接：60 分鐘 (清潔消毒/雙人盤點)\n👉 真正能開車搬運的時間整整只有 600 分鐘！",
         DARK_BLUE),
        ("② 搬運動線硬約束：電梯與長推吞噬工時", 
         "各站實體動線具有不可壓縮的物理下限：\n▪ 8CD / 8F 垂直貨梯換車：硬性耗時 20~25 分鐘\n▪ 8S 碼頭至 8S5A 庫房：純長推耗時 35~50 分鐘\n▪ 廠際道路行車：近距 5 分鐘，遠距 10~15 分鐘",
         PRIMARY_BLUE),
        ("③ 車廂空間硬約束：環廠死鎖矛盾 (Deadlock)", 
         "若巡迴車在前站載滿 40 批，中後站將完全無空間上貨：\n▪ 導致中繼站物料滯留拒載、碼頭癱瘓\n👉 鐵律規範：中繼在途嚴控 ≤ 16 批 (留 24 批空位)\n👉 單站單點配額上限 ≤ 24 批，防止大站獨佔",
         HIGHLIGHT_ORANGE)
    ]

    for i, (c_title, c_desc, c_col) in enumerate(constraints):
        c_top = Inches(1.6 + i * 1.8)
        card = create_card(s3, Inches(0.8), c_top, Inches(11.7), Inches(1.6))
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.18)
        tf.margin_left = tf.margin_right = Inches(0.3)
        
        p = tf.paragraphs[0]
        p.text = c_title
        p.font.name = FONT_MAIN
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = c_col
        
        for line in c_desc.split('\n'):
            p_sub = tf.add_paragraph()
            p_sub.text = line
            p_sub.font.name = FONT_MAIN
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = DARK_TEXT
            p_sub.space_before = Pt(2)

    # =========================================================================
    # SLIDE 4: 什麼叫做一個「好的車班表」？ (The Evaluation Metrics)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "04 | 什麼叫好班表？現場做得出、零拒載、等候最短的動態平衡", "OPTIMIZATION OBJECTIVE & METRICS")

    metrics = [
        ("1. 現場可執行性 (Feasibility)", "做得出來", HIGHLIGHT_GREEN,
         "● 100% 尊重電梯與長推物理動線\n● 8CD/8F 給足 25m、8S 給足 40m\n● 不排不切實際的瞬間閃電發車\n● 實際班表準點率達到 95% 以上"),

        ("2. 全系統零拒載 (Zero Deadlock)", "零卡車", PRIMARY_BLUE,
         "● 落實專車大單與巡迴散單嚴格分流\n● 環廠航段隨時維持 60% 車廂淨空\n● 任何廠區有急件，到站即有空間可上\n● 全廠區拒載率壓降至 0%"),

        ("3. 出貨候車最短 (Service Level)", "隨到隨發", ACCENT_BLUE,
         "● 全日班次呈定時脈衝均勻分佈\n● FAB8F 發車班距 17m (等候 8.5m)\n● FAB8CD 發車班距 19m (等候 9.5m)\n● 全廠平均候車壓縮至 8~20 分鐘"),

        ("4. 時間軸透明有序 (Clarity)", "單一總表", DARK_BLUE,
         "● 日班 89 趟按發車時刻嚴格排序\n● 統一四大欄位：車號/出發站/作業/行車\n● 生管庫房一眼看懂、精準備貨\n● 徹底消除跨廠聯絡誤差")
    ]

    for i, (m_title, m_tag, m_col, m_body) in enumerate(metrics):
        r = i // 2
        c = i % 2
        left = Inches(0.8 + c * 5.9)
        top = Inches(1.6 + r * 2.7)
        card = create_card(s4, left, top, Inches(5.8), Inches(2.5))
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.18)
        tf.margin_left = tf.margin_right = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_MAIN
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = m_col
        
        p_tag = tf.add_paragraph()
        p_tag.text = f"【核心指標：{m_tag}】"
        p_tag.font.name = FONT_MAIN
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = DARK_TEXT
        p_tag.space_before = Pt(2)
        p_tag.space_after = Pt(6)

        for line in m_body.split('\n'):
            p_b = tf.add_paragraph()
            p_b.text = line
            p_b.font.name = FONT_MAIN
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = DARK_TEXT
            p_b.space_before = Pt(1)

    # =========================================================================
    # SLIDE 5: 什麼叫做「運能」？雙解放突破 (Capacity Breakthrough)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "05 | 什麼叫運能？跳脫紙上數字，雙解放機制推升全廠達 4,608 批/天", "TRUE CAPACITY & BREAKTHROUGH")

    # Left Box: Definition & 2 Relief Mechanisms
    left_card = create_card(s5, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.3))
    tf_l = left_card.text_frame
    tf_l.word_wrap = True
    tf_l.margin_top = Inches(0.2)
    tf_l.margin_left = tf_l.margin_right = Inches(0.25)

    p_l1 = tf_l.paragraphs[0]
    p_l1.text = "運能的真實本質 (Throughput)"
    p_l1.font.name = FONT_MAIN
    p_l1.font.size = Pt(15)
    p_l1.font.bold = True
    p_l1.font.color.rgb = PRIMARY_BLUE

    p_l2 = tf_l.add_paragraph()
    p_l2.text = "運能絕非『40批 × 趟數』的死乘法！而是『在不拒載約束下，實際成功送達目的地的有效批次總和』。"
    p_l2.font.name = FONT_MAIN
    p_l2.font.size = Pt(11)
    p_l2.font.color.rgb = DARK_TEXT
    p_l2.space_before = Pt(6)
    p_l2.space_after = Pt(14)

    p_l3 = tf_l.add_paragraph()
    p_l3.text = "🌟 本研究兩大運能解放機制："
    p_l3.font.name = FONT_MAIN
    p_l3.font.size = Pt(13)
    p_l3.font.bold = True
    p_l3.font.color.rgb = HIGHLIGHT_ORANGE
    p_l3.space_after = Pt(8)

    p_l4 = tf_l.add_paragraph()
    p_l4.text = "1. 終點航段解放 (Terminal Relaxation)\n開往巡迴終點前一航段，進站即全卸，直接解除 16 批限制，放寬至 40 批滿載！"
    p_l4.font.name = FONT_MAIN
    p_l4.font.size = Pt(10.5)
    p_l4.font.color.rgb = DARK_TEXT
    p_l4.space_after = Pt(10)

    p_l5 = tf_l.add_paragraph()
    p_l5.text = "2. 午休跨休預載專車 (Preload)\n利用 60m 用餐停靠，離站前預載滿 40 批直送下午首站，憑空多創造 1 趟專車運能！"
    p_l5.font.name = FONT_MAIN
    p_l5.font.size = Pt(10.5)
    p_l5.font.color.rgb = DARK_TEXT

    # Right Box: Full Fleet 24H Capacity Table
    t_shape2 = s5.shapes.add_table(7, 5, Inches(5.5), Inches(1.6), Inches(7.0), Inches(5.3))
    t2 = t_shape2.table
    t2.columns[0].width = Inches(1.3)
    t2.columns[1].width = Inches(1.4)
    t2.columns[2].width = Inches(1.8)
    t2.columns[3].width = Inches(1.2)
    t2.columns[4].width = Inches(1.3)

    c_headers = ["車輛編號", "母港基地", "核心功能定位", "單班運能", "24H 總運能"]
    for col_idx, h in enumerate(c_headers):
        cell = t2.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_MAIN
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    fleet_capacity = [
        ("Car A", "FAB8E 大廳", "外廠專營 ＋ 全廠巡迴", "360 批", "720 批"),
        ("Car B", "FAB8F 代工", "8F 母港專車 ＋ 小環", "600 批", "1,200 批 (冠)"),
        ("Car C", "FAB8AB 大廳", "力行心臟 ＋ 8F 對開", "520 批", "1,040 批"),
        ("Car D", "FAB8CD 碼頭", "全日純環廠巡迴毛細管", "344 批", "688 批"),
        ("Car E", "FAB8S 庫房", "庫房專車 ＋ 外圍接駁", "480 批", "960 批"),
        ("全車隊", "五大母港", "全日實體位移 178 趟", "2,304 批", "4,608 批/天")
    ]

    for row_idx, r_data in enumerate(fleet_capacity, start=1):
        for col_idx, text in enumerate(r_data):
            cell = t2.cell(row_idx, col_idx)
            cell.fill.solid()
            if row_idx == 6:
                cell.fill.fore_color.rgb = RGBColor(254, 243, 199) # Gold highlight
            else:
                cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_MAIN
            p.font.size = Pt(11 if row_idx == 6 else 10)
            p.font.color.rgb = HIGHLIGHT_ORANGE if row_idx == 6 else DARK_TEXT
            if col_idx in [0, 3, 4] or row_idx == 6:
                p.font.bold = True
            p.alignment = PP_ALIGN.CENTER

    ppt_path = "g:/我的雲端硬碟/AI/Logistics/半導體廠區物流運籌系統問題與運能分析.pptx"
    prs.save(ppt_path)
    print("PowerPoint deck successfully generated at:", ppt_path)

if __name__ == '__main__':
    create_deck()
