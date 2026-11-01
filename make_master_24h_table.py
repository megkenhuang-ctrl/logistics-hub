import json, sys

with open('g:/我的雲端硬碟/AI/Logistics/all_cars_24h_chronological.json', 'r', encoding='utf-8') as f:
    deps = json.load(f)

lines = []
lines.append('# 🕒 全車隊 24 小時連續發車時間軸總表（Master 24-Hour Fleet Chronological Schedule）')
lines.append('> [!IMPORTANT]')
lines.append('> **本表為全廠區 24 小時（日班 07:35~19:35 ＋ 夜班 19:35~07:35 鏡像對稱）車隊物流運籌之最終總綱**。')
lines.append('> 涵蓋 **Car A、Car B、Car C、Car D、Car E** 全車隊所有實體位移班次，**嚴格依據「發車時刻（Departure Time）」由晨間 07:55 連續排序至次日早晨 06:40**。')
lines.append('> 完整統一 4 大關鍵管理欄位：**`車輛編號`**、**`出發站 (Origin)`**、**`作業時間 (Dwell)`**、**`行車時間 (Transit)`**。')
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

out_path = 'C:/Users/cr_hu/.gemini/antigravity/brain/a3f48c0d-fb64-4ddf-8cef-7413e76ac8cb/master_fleet_24h_chronological_schedule.md'
with open(out_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(lines))

print('Master 24H table written successfully, total rows:', len(lines))
