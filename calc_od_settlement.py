import sqlite3, sys, json
if hasattr(sys.stdout, 'reconfigure'): 
    sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('logistics.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

rows = cursor.execute('SELECT car_name, shift, fab_code, mode, od_flow, capacity_batches FROM schedules WHERE is_break = 0').fetchall()

def normalize_fab(f):
    if not f: return None
    clean = f.strip().replace('*', '').replace('🟦', '')
    if '8AB' in clean or clean == '8AB' or clean == 'AB': return 'FAB8AB'
    if '8CD' in clean or clean == '8CD' or clean == 'CD': return 'FAB8CD'
    if '8E' in clean or clean == '8E' or clean == 'E': return 'FAB8E'
    if '8F' in clean or clean == '8F' or clean == 'F': return 'FAB8F'
    if '8S' in clean or clean == '8S' or clean == 'S': return 'FAB8S'
    if '篤行' in clean: return '嘉晶篤行'
    if '創新' in clean: return '嘉晶創新'
    return clean

fabs = ['FAB8AB', 'FAB8CD', 'FAB8E', 'FAB8F', 'FAB8S', '嘉晶篤行', '嘉晶創新']
od_day = {}
od_24h = {}
outbound_24h = {}
inbound_24h = {}
car_contributions_24h = {}

for r in rows:
    shift = r['shift']
    car = r['car_name']
    cap = r['capacity_batches']
    dock_fab = normalize_fab(r['fab_code'])
    od_raw = r['od_flow'] or ''

    lines = [ln.strip() for ln in od_raw.split('<br>') if '在途' not in ln and '➔' in ln]
    if not lines:
        continue
    cap_per_line = cap // len(lines)

    for ln in lines:
        parts = ln.split('➔')
        orig = normalize_fab(parts[0])
        if not orig or orig not in fabs:
            orig = dock_fab

        dests = [normalize_fab(x) for x in parts[1].split('/')]
        dests = [d for d in dests if d in fabs and d != orig]
        if not dests:
            continue

        cap_each = cap_per_line // len(dests)

        for d in dests:
            p = (orig, d)
            if p not in od_24h: od_24h[p] = {'trips': 0, 'cap': 0, 'cars': set()}
            od_24h[p]['trips'] += 1
            od_24h[p]['cap'] += cap_each
            od_24h[p]['cars'].add(car)

            outbound_24h[orig] = outbound_24h.get(orig, 0) + cap_each
            inbound_24h[d] = inbound_24h.get(d, 0) + cap_each

            if car not in car_contributions_24h: car_contributions_24h[car] = {'trips': 0, 'cap': 0}
            car_contributions_24h[car]['trips'] += 1
            car_contributions_24h[car]['cap'] += cap_each

            if shift == 'day':
                if p not in od_day: od_day[p] = {'trips': 0, 'cap': 0, 'cars': set()}
                od_day[p]['trips'] += 1
                od_day[p]['cap'] += cap_each
                od_day[p]['cars'].add(car)

print("====================================================================================")
print("          廠區全車隊 24H 全日 From-To (OD) 運能結算 vs. Demand_from_to.xlsx         ")
print("====================================================================================")
total_trips_24 = sum(v['trips'] for v in od_24h.values())
total_cap_24 = sum(v['cap'] for v in od_24h.values())
print(f"總結算：全日 24H 共排定 {total_trips_24} 趟次跨廠物料輸送，總跨廠 OD 供給運能達 {total_cap_24} 批次。\n")

demands = cursor.execute('SELECT from_fab, to_fab, demand_batches, demand_shift_batches FROM demand_matrix ORDER BY id').fetchall()
demand_map = {(r['from_fab'], r['to_fab']): r['demand_batches'] for r in demands}

print(f"{'起點 (From)':10s} ➔ {'迄點 (To)':10s} | {'24H基準需求':>10s} | {'24H排程班次':>10s} | {'24H供給運能':>10s} | {'滿足率':>8s} | 服務車隊")
print("-" * 92)
for r in demands:
    o, d, req24 = r['from_fab'], r['to_fab'], r['demand_batches']
    actual = od_24h.get((o, d), {'trips': 0, 'cap': 0, 'cars': set()})
    act_t = actual['trips']
    act_c = actual['cap']
    pct = (act_c / req24 * 100) if req24 > 0 else 0
    cars_str = ', '.join(sorted(list(actual['cars']))) if actual['cars'] else '環廠中繼順道'
    print(f"{o:12s} ➔ {d:10s} | {req24:8d} 批 | {act_t:8d} 趟 | {act_c:8d} 批 | {pct:6.1f}% | {cars_str}")

print("\n====================================================================================")
print("          各廠區 24H 發出/接收 OD 運能 vs. Demand_from_to.xlsx (OD Sum & Col J Sum)  ")
print("====================================================================================")
fab_rows = cursor.execute('SELECT code, demand_out_24h, demand_in_24h, demand_excel_sum FROM fabs').fetchall()
print(f"{'廠區名稱':10s} | {'OD發出需求':>10s} | {'24H發出供給':>10s} | {'24H接收供給':>10s} | {'Excel總量(J欄)':>12s} | {'全日到站總運能':>12s} | {'總量滿足率':>8s}")
print("-" * 95)
for fr in fab_rows:
    f = fr['code']
    out_c = outbound_24h.get(f, 0)
    in_c = inbound_24h.get(f, 0)
    tot_stop_cap = cursor.execute('SELECT sum(capacity_batches) FROM schedules WHERE fab_code=? AND is_break=0', (f,)).fetchone()[0] or 0
    excel_sum = fr['demand_excel_sum']
    pct = (tot_stop_cap / excel_sum * 100) if excel_sum > 0 else 0
    print(f"{f:10s} | {fr['demand_out_24h']:8d} 批 | {out_c:8d} 批 | {in_c:8d} 批 | {excel_sum:10d} 批 | {tot_stop_cap:10d} 批 | {pct:7.1f}%")
