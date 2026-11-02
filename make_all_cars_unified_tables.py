import sys, re

# Read Car B from line176_B_full.md
with open('g:/我的雲端硬碟/AI/Logistics/line176_B_full.md', 'r', encoding='utf-8') as f:
    b_raw = f.read()

# Read Car A, C, D, E from line222_ACDE.md
with open('g:/我的雲端硬碟/AI/Logistics/line222_ACDE.md', 'r', encoding='utf-8') as f:
    acde_raw = f.read()

def clean_cell(c):
    return c.strip()

output_docs = {}

# Standard Master Columns:
# | 車輛編號 | 站次 | 停靠廠區與作業位置 | 營運模式 | OD (物料起迄流向) | 日班時間 (到 - 離) | 夜班時間 (到 - 離) | 作業時間 (Dwell) | 行車時間 (Transit) | 📦 上下貨與在途載量指令 (防呆關鍵) | 現場執行重點與 SOP |

# --- Process Car A ---
a_sec = acde_raw.split('# 🚗 【Car A 車班表】')[1].split('# 🚗 【Car C 車班表】')[0]
a_rows = [l.strip() for l in a_sec.split('\n') if l.strip().startswith('| **') or l.strip().startswith('| 🟦 **')]
a_table = []
for r in a_rows:
    cols = [clean_cell(c) for c in r.split('|')[1:-1]]
    # cols: st_no, loc, mode, od, day_t, night_t, dwell, transit, cmd, sop
    st_no, loc, mode, od, day_t, night_t, dwell, transit, cmd, sop = cols[:10]
    a_table.append(f'| **Car A** | {st_no} | {loc} | {mode} | {od} | {day_t} | {night_t} | {dwell} | {transit} | {cmd} | {sop} |')
output_docs['Car_A'] = a_table

# --- Process Car B ---
b_rows = [l.strip() for l in b_raw.split('\n') if l.strip().startswith('| **') or l.strip().startswith('| 🟦 **')]
b_table = []
for r in b_rows:
    cols = [clean_cell(c) for c in r.split('|')[1:-1]]
    # cols: st_no, loc, mode, od, day_t, dwell, transit, cmd, sop
    st_no = cols[0]
    loc = cols[1]
    mode = cols[2]
    od = cols[3]
    day_t = cols[4]
    dwell = cols[5]
    transit = cols[6]
    cmd = cols[7]
    sop = cols[8]
    
    # Calculate Night Shift (+12h)
    times = re.findall(r'\d{2}:\d{2}', day_t)
    if len(times) == 2:
        ah, am = map(int, times[0].split(':'))
        dh, dm = map(int, times[1].split(':'))
        night_t = f'{(ah+12)%24:02d}:{am:02d} - {(dh+12)%24:02d}:{dm:02d}'
    else:
        night_t = '—'
        
    b_table.append(f'| **Car B** | {st_no} | {loc} | {mode} | {od} | {day_t} | {night_t} | {dwell} | {transit} | {cmd} | {sop} |')
output_docs['Car_B'] = b_table

# --- Process Car C ---
c_sec = acde_raw.split('# 🚗 【Car C 車班表】')[1].split('# 🚗 【Car D 車班表】')[0]
c_rows = [l.strip() for l in c_sec.split('\n') if l.strip().startswith('| **') or l.strip().startswith('| 🟦 **')]
c_table = []
for r in c_rows:
    cols = [clean_cell(c) for c in r.split('|')[1:-1]]
    st_no, loc, mode, od, day_t, night_t, dwell, transit, cmd, sop = cols[:10]
    c_table.append(f'| **Car C** | {st_no} | {loc} | {mode} | {od} | {day_t} | {night_t} | {dwell} | {transit} | {cmd} | {sop} |')
output_docs['Car_C'] = c_table

# --- Process Car D ---
d_sec = acde_raw.split('# 🚗 【Car D 車班表】')[1].split('# 🚗 【Car E 車班表】')[0]
d_rows = [l.strip() for l in d_sec.split('\n') if l.strip().startswith('| **') or l.strip().startswith('| 🟦 **')]
d_table = []
for r in d_rows:
    cols = [clean_cell(c) for c in r.split('|')[1:-1]]
    st_no, loc, mode, od, day_t, night_t, dwell, transit, cmd, sop = cols[:10]
    d_table.append(f'| **Car D** | {st_no} | {loc} | {mode} | {od} | {day_t} | {night_t} | {dwell} | {transit} | {cmd} | {sop} |')
output_docs['Car_D'] = d_table

# --- Process Car E ---
e_sec = acde_raw.split('# 🚗 【Car E 車班表】')[1].split('### 全車隊總覽對照備忘錄')[0]
e_rows = [l.strip() for l in e_sec.split('\n') if l.strip().startswith('| **') or l.strip().startswith('| 🟦 **')]
e_table = []
for r in e_rows:
    cols = [clean_cell(c) for c in r.split('|')[1:-1]]
    # cols: st_no, loc, mode, od, day_t, dwell, transit, cmd, sop
    st_no = cols[0]
    loc = cols[1]
    mode = cols[2]
    od = cols[3]
    day_t = cols[4]
    dwell = cols[5]
    transit = cols[6]
    cmd = cols[7]
    sop = cols[8]
    times = re.findall(r'\d{2}:\d{2}', day_t)
    if len(times) == 2:
        ah, am = map(int, times[0].split(':'))
        dh, dm = map(int, times[1].split(':'))
        night_t = f'{(ah+12)%24:02d}:{am:02d} - {(dh+12)%24:02d}:{dm:02d}'
    else:
        night_t = '—'
    e_table.append(f'| **Car E** | {st_no} | {loc} | {mode} | {od} | {day_t} | {night_t} | {dwell} | {transit} | {cmd} | {sop} |')
output_docs['Car_E'] = e_table

# --- Process Car U (from U_Car.PNG 10/05版) ---
u_table = [
    '| **Car U** | **1** | **FAB8S**<br>1F 碼頭/8S5A | **專車** | **8S ➔ 8F** | 07:35 - 08:30 | 19:35 - 20:30 | **55 mins** | **20 mins** | **【專車直達】可滿載 40 批**<br>➔ 全上 [8S ➔ 8F] 庫房物料（8S保持原作法） | 母站 8S 始發深度裝載 55 分鐘，08:30/20:30 準時發車（代工組 8659045）。 |',
    '| **Car U** | **2** | **FAB8F**<br>3F 代工出入口 | **專車** | **8F ➔ 8CD** | 08:50 - 09:15 | 20:50 - 21:15 | **25 mins** | **5 mins** | **【專車直達】可滿載 40 批**<br>➔ 卸 [8S➔8F]，3F 換車全上 [8F ➔ 8CD] | 8F @3F 換車作業（代工組 8658575），點對點不跨趟次收。 |',
    '| **Car U** | **3** | **FAB8CD**<br>裝卸碼頭上 3F | **專車** | **8CD ➔ 8E** | 09:20 - 09:50 | 21:20 - 21:50 | **30 mins** | **10 mins** | **【專車直達】可滿載 40 批**<br>➔ 卸 [8F➔8CD]，3F 換車全上 [8CD ➔ 8E] | 8C/8D @3F 換車作業（8C:8676442 / 8D:8639103）。 |',
    '| **Car U** | **4** | **FAB8E**<br>1F 大廳 | **專車** | **8E ➔ 8S** | 10:00 - 10:25 | 22:00 - 22:25 | **25 mins** | **10 mins** | **【專車直達】可滿載 40 批**<br>➔ 卸 [8CD➔8E]，1F 換車全上 [8E ➔ 8S] | 8E @1F 換車作業（代工組 8656986 & 8656233）。 |',
    '| **Car U** | **5** | **FAB8S**<br>1F 碼頭/8S5A | **專車** | **8S ➔ 8F** | 10:35 - 11:20 | 22:35 - 23:20 | **45 mins** | **15 mins** | **【專車直達】可滿載 40 批**<br>➔ 卸 [8E➔8S]，全上 [8S ➔ 8F] 庫房物料 | 8S @1F 保持原作法深度裝卸 45 分鐘。 |',
    '| **Car U** | **6** | **FAB8F**<br>3F 代工出入口 | **專車** | **8F (午休卸清)** | 11:35 - 12:00 | 23:35 - 00:00 | **25 mins** | **0 min** | **【專車到站全卸】車廂清空**<br>➔ 卸下 [8S➔8F] 物料，車廂完全清空 | 8F @3F 卸貨完畢，12:00/00:00 準時停妥進入同仁用餐。 |',
    '| **Car U** | **7** | **同仁用餐** | **休息** | **—** | 12:00 - 13:00 | 00:00 - 01:00 | **60 mins** | **0 min** | **【同仁安心用餐 60 分鐘】** | 司機完整休息用餐 60 分鐘，用餐後前往 8AB。 |',
    '| **Car U** | **8** | **FAB8AB**<br>1F 大廳 | **專車** | **8AB ➔ 8E** | 13:00 - 13:25 | 01:00 - 01:25 | **25 mins** | **5 mins** | **【午後專車重啟】可滿載 40 批**<br>➔ 1F 換貨全上 [8AB ➔ 8E] 物料 | 8AB @1F 為換貨作業（代工組 8633382 & 8637773）。 |',
    '| **Car U** | **9** | **FAB8E**<br>1F 大廳 | **專車** | **8E ➔ 8CD** | 13:30 - 13:50 | 01:30 - 01:50 | **20 mins** | **10 mins** | **【專車直達】可滿載 40 批**<br>➔ 卸 [8AB➔8E]，1F 換車全上 [8E ➔ 8CD] | 8E @1F 換車作業，點對點直達 8CD。 |',
    '| **Car U** | **10** | **FAB8CD**<br>裝卸碼頭上 3F | **專車** | **8CD ➔ 8F** | 14:00 - 14:15 | 02:00 - 02:15 | **15 mins** | **5 mins** | **【專車直達】可滿載 40 批**<br>➔ 卸 [8E➔8CD]，3F 快速換車全上 [8CD ➔ 8F] | 8CD @3F 緊湊換車 15 分鐘，直奔 8F。 |',
    '| **Car U** | **11** | **FAB8F**<br>3F 代工出入口 | **專車** | **8F ➔ 8CD** | 14:20 - 14:45 | 02:20 - 02:45 | **25 mins** | **5 mins** | **【專車直達】可滿載 40 批**<br>➔ 卸 [8CD➔8F]，3F 換車全上 [8F ➔ 8CD] | 8F ➔ 8CD 午後高頻專車對開第 1 趟。 |',
    '| **Car U** | **12** | **FAB8CD**<br>裝卸碼頭上 3F | **專車** | **8CD ➔ 8F** | 14:50 - 15:15 | 02:50 - 03:15 | **25 mins** | **5 mins** | **【專車直達】可滿載 40 批**<br>➔ 卸 [8F➔8CD]，3F 換車全上 [8CD ➔ 8F] | 8CD ➔ 8F 午後高頻專車對開第 2 趟。 |',
    '| **Car U** | **13** | 🟦 **FAB8F**<br>3F 代工出入口 | **小環** | **8F ➔ 8S**<br>**8F ➔ 8AB** *(跨)* | 15:20 - 15:50 | 03:20 - 03:50 | **30 mins** | **10 mins** | **【藍色框小環起點】單站上限 24 批**<br>➔ 卸 [8CD➔8F]，收往下 2~3 站（8S/8AB/8E）最少留 24 批位 | 進入藍色框環廠模式，單站到同一站最多一次上 24 批。 |',
    '| **Car U** | **14** | 🟦 **FAB8S**<br>1F 碼頭/8S5A | **小環** | **8S ➔ 8AB** | 16:00 - 16:40 | 04:00 - 04:40 | **40 mins** | **0 min** | **【小環中繼】單站上限 24 批**<br>➔ 卸 [8F➔8S]，收往下 2~3 站（8AB/8E/8CD）最少留 24 批位 | 8S @1F 保持原作法裝卸 40 分鐘，完畢後原地或順路用餐。 |',
    '| **Car U** | **15** | 🟦 **同仁用餐** | **休息** | **—** | 16:40 - 17:30 | 04:40 - 05:30 | **50 mins** | **0 min** | **【同仁用餐 50 分鐘（小環跨休）】** | 藍色框小環期間用餐 50 分鐘，17:30/05:30 準時抵達 8AB。 |',
    '| **Car U** | **16** | 🟦 **FAB8AB**<br>1F 大廳 | **小環** | **8AB ➔ 8E** | 17:30 - 17:50 | 05:30 - 05:50 | **20 mins** | **5 mins** | **【黃底重點站・小環換貨】單站上限 24 批**<br>➔ 卸貨，1F 換貨收往 8E / 8CD 物料（最少留 24 批位） | 黃底重點提醒站：8AB @1F 換貨 20 分鐘。 |',
    '| **Car U** | **17** | 🟦 **FAB8E**<br>1F 大廳 | **小環** | **8E ➔ 8CD** | 17:55 - 18:15 | 05:55 - 06:15 | **20 mins** | **10 mins** | **【小環終點航段解放】單站上限 24 批**<br>➔ 卸貨，1F 換車全上 [8E ➔ 8CD] 物料 | 下一站 8CD 為藍色框環廠終點站。 |',
    '| **Car U** | **18** | 🟦 **FAB8CD**<br>裝卸碼頭上 3F | **小環** | **8CD (全日清空)** | 18:25 - 18:40 | 06:25 - 06:40 | **15 mins** | **0 min** | **【藍色框小環終點】全部下貨清空**<br>➔ 卸下所有在途物料，車廂完全清空 | 18:40/06:40 於 8CD 卸清，進入交接整理。 |',
    '| **Car U** | **19** | **同仁交接整理** | **交接** | **— (任務完成)** | 18:40 - 19:00 | 06:40 - 07:00 | **20 mins** | **—** | **【同仁交接整理 20 分鐘】** | 車廂巡檢清潔、台車歸位與交接整理（19:00/07:00 完畢）。 |'
]
output_docs['Car_U'] = u_table


# Now generate the combined master markdown file
header = '''# 🚚 全車隊逐站標準執行車班總表（Unified Fleet Master Schedules）

> [!IMPORTANT]
> **本文件已將全車隊（Car A、Car B、Car C、Car D、Car E）所有車班表全面格式統一**。
> 所有車輛均包含完整的 **11 大標準作業欄位**：
> `車輛編號`、`站次`、`停靠廠區與作業位置`、`營運模式`、`OD (物料起迄流向)`、`日班時間`、`夜班時間`、`作業時間 (Dwell)`、`行車時間 (Transit)`、`上下貨與在途載量指令 (防呆關鍵)`、`現場執行重點與 SOP`。

---
'''

table_hdr = '''| 車輛編號 | 站次 | 停靠廠區與作業位置 | 營運模式 | **OD (物料起迄流向)** | 日班時間 (到 - 離) | 夜班時間 (到 - 離) | **作業時間 (Dwell)** | **行車時間 (Transit)** | 📦 上下貨與在途載量指令 (防呆關鍵) | 現場執行重點與 SOP |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
'''

full_text = [header]

car_meta = {
    'Car_A': ('Car A 車班表（外廠門戶與全廠巡迴旗艦）', 'FAB8E 1F 大廳', '8644824（0960-717239）', '640 批'),
    'Car_B': ('Car B 車班表（FAB8F 代工母港主動脈專車）', 'FAB8F 代工出入口', '8644828（0960-717178）', '600 批'),
    'Car_C': ('Car C 車班表（FAB8AB 力行心臟與 8F 密集對開）', 'FAB8AB 1F 大廳', '8644830（0960-717258）', '520 批'),
    'Car_D': ('Car D 車班表（FAB8CD 母港全日純環廠巡迴車）', 'FAB8CD 裝卸碼頭上 3F', '8681029（0965-702916）', '344 批'),
    'Car_E': ('Car E 車班表（FAB8S 庫房母港專車與小環）', 'FAB8S 1F 碼頭/8S5A', '8681030（0965-702918）', '480 批'),
    'Car_U': ('Car U 車班表（聯電同仁支援加班車・專車+小環）', 'FAB8S 1F 碼頭/8S5A', '8638834（0975-612990）', '496 批')
}

for c_key in ['Car_A', 'Car_B', 'Car_C', 'Car_D', 'Car_E', 'Car_U']:
    title, hub, phone, cap = car_meta[c_key]
    full_text.append(f'## 🚗 【{title}】')
    full_text.append(f'* **車輛母站**：**{hub}** ｜ **專線簡碼**：{phone}')
    full_text.append(f'* **生效時段**：日班 07:35 ～ 19:35 ｜ 夜班 19:35 ～ 07:35（+12 小時精確對稱）')
    full_text.append(f'* **單班目標總運能**：**{cap}**')
    full_text.append('')
    full_text.append(table_hdr + '\n'.join(output_docs[c_key]))
    full_text.append('\n---\n')

master_path = 'C:/Users/cr_hu/.gemini/antigravity/brain/a3f48c0d-fb64-4ddf-8cef-7413e76ac8cb/master_unified_all_cars_schedules.md'
with open(master_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(full_text))

print('Master Unified Schedules written successfully! Total cars: 5')
