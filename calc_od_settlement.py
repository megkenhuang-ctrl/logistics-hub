import sqlite3, sys, json
from validator import parse_od_pairs
if hasattr(sys.stdout, 'reconfigure'): 
    sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('logistics.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

fabs = ['FAB8AB', 'FAB8CD', 'FAB8E', 'FAB8F', 'FAB8S', '嘉晶篤行', '嘉晶創新']
demands = [dict(r) for r in cursor.execute('SELECT from_fab, to_fab, demand_batches, demand_shift_batches FROM demand_matrix ORDER BY demand_batches DESC, from_fab, to_fab').fetchall()]
fab_rows = [dict(r) for r in cursor.execute('SELECT code, demand_out_24h, demand_in_24h, demand_excel_sum FROM fabs').fetchall()]

for tbl, title in [('schedules', '原方案 (Baseline)'), ('schedules_plan2', '方案二 (CP-SAT 雙層優化)'), ('schedules_plan3', '方案三 (100% 剛性合規版)')]:
    rows = [dict(r) for r in cursor.execute(f"SELECT * FROM {tbl} WHERE is_break = 0 AND car_id != 'Car_U'").fetchall()]
    od_24h = {}
    outbound_24h = {}
    inbound_24h = {}
    for r in rows:
        car = r['car_name']
        for orig, d, cap_each in parse_od_pairs(r):
            if orig in fabs and d in fabs and orig != d:
                p = (orig, d)
                if p not in od_24h:
                    od_24h[p] = {'trips': 0, 'cap': 0, 'cars': set()}
                od_24h[p]['trips'] += 1
                od_24h[p]['cap'] += cap_each
                od_24h[p]['cars'].add(car)
                outbound_24h[orig] = outbound_24h.get(orig, 0) + cap_each
                inbound_24h[d] = inbound_24h.get(d, 0) + cap_each

    print("\n==============================================================================================")
    print(f"   [{title}] 廠區全車隊 24H 全日 From-To (OD) 運能結算 vs. Demand_from_to.xlsx (5,742 批)")
    print("==============================================================================================")
    total_trips_24 = sum(v['trips'] for v in od_24h.values())
    total_cap_24 = sum(v['cap'] for v in od_24h.values())
    print(f"總結算：全日 24H 共排定 {total_trips_24} 筆跨廠 OD 紀錄，總跨廠 OD 供給運能達 {total_cap_24} 批次。\n")

    print(f"{'起點 (From)':10s} ➔ {'迄點 (To)':10s} | {'24H基準需求':>10s} | {'24H排程班次':>10s} | {'24H供給運能':>10s} | {'走廊利用率':>8s} | {'合規狀態':>8s} | 服務車隊")
    print("-" * 102)
    for r in demands:
        o, d, req24 = r['from_fab'], r['to_fab'], r['demand_batches']
        if req24 <= 0:
            continue
        actual = od_24h.get((o, d), {'trips': 0, 'cap': 0, 'cars': set()})
        act_t = actual['trips']
        act_c = actual['cap']
        util_pct = (req24 / act_c * 100) if act_c > 0 else 999.9
        status = 'PASS' if util_pct <= 85.0 else 'FAIL'
        cars_str = ', '.join(sorted(list(actual['cars']))) if actual['cars'] else '-'
        print(f"{o:12s} ➔ {d:10s} | {req24:8d} 批 | {act_t:8d} 趟 | {act_c:8d} 批 | {util_pct:7.1f}% | {status:>8s} | {cars_str}")
