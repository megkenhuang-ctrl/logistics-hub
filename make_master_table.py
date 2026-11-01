import json, sys

with open('g:/我的雲端硬碟/AI/Logistics/all_cars_chronological.json', 'r', encoding='utf-8') as f:
    deps = json.load(f)

lines = []
lines.append('# 🕒 全車隊發車時間軸總表（Master Chronological Departure Schedule）')
lines.append('> [!NOTE]')
lines.append('> 本表涵蓋 **Car A、Car B、Car C、Car D、Car E** 全車隊所有實體班次，**嚴格依據「發車時刻（Departure Time）」進行全日時間軸排序**。')
lines.append('> 包含標準 4 大必備欄位：**`車輛編號`**、**`出發站 (Origin)`**、**`作業時間 (Dwell)`**、**`行車時間 (Transit)`**。')
lines.append('')
lines.append('| 發車時刻 | 車輛編號 | 班別 | 站次 | 出發站 (Origin) | 停靠作業時間 | 作業時間 (Dwell) | 行車時間 (Transit) | 目標目的地 (Destination) | 營運模式 | 📦 上下貨與在途載量指令 (防呆關鍵) |')
lines.append('| :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- | :---: | :--- |')

for d in deps:
    c = d['car']
    s = d['shift']
    st = d['stop_no']
    orig = d['origin']
    tr = d['time_range']
    dw = d['dwell']
    tt = d['transit']
    dt = f"**{d['dep_time']}**"
    dest = d['dest']
    mode = d['mode']
    cmd = d['cmd'].replace('|', '/')
    lines.append(f'| {dt} | **{c}** | {s} | {st} | {orig} | {tr} | {dw} | {tt} | **{dest}** | {mode} | {cmd} |')

out_path = 'C:/Users/cr_hu/.gemini/antigravity/brain/a3f48c0d-fb64-4ddf-8cef-7413e76ac8cb/master_fleet_chronological_schedule.md'
with open(out_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(lines))

print('Master table written successfully, total rows:', len(lines))
