# -*- coding: utf-8 -*-
"""
半導體廠區物流排程 - 實際營運出勤與動態運能計算引擎 (Actual Operations Engine)
關聯司機每日班表 (driver_roster)，將出勤車輛（含 Car U）之動態運能與走廊需求即時比對，
精確計算當班/當日走廊利用率並標記 Overloading 斷料風險。
"""

import sqlite3
import re
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from validator import parse_od_pairs, norm_fab

DB_PATH = os.path.join(BASE_DIR, 'logistics.db')

def evaluate_actual_operations(db_path=DB_PATH, date_str='2026-11-01', shift='all', table_name='schedules'):
    """
    動態營運模式評估核心
    :param db_path: SQLite 資料庫路徑
    :param date_str: 營運日期 (YYYY-MM-DD)
    :param shift: 班別 ('all', 'day', 'night')
    :param table_name: 基準排程表 ('schedules_plan3', 'schedules_plan2', 'schedules')
    """
    if table_name not in ['schedules', 'schedules_plan2', 'schedules_plan3']:
        table_name = 'schedules_plan3'

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # 1. 查詢司機排班出勤狀態
    roster_query = "SELECT * FROM driver_roster WHERE date = ?"
    roster_args = [date_str]
    if shift in ['day', 'night']:
        roster_query += " AND lower(shift) = ?"
        roster_args.append(shift)

    roster_rows = conn.execute(roster_query, roster_args).fetchall()
    
    active_cars = set()
    car_roster_map = {}
    
    # 支援全日模式下的車輛統計
    for r in roster_rows:
        cid = r['car_id']
        # 全日模式下若某車在任一班次有執勤，則標註有出勤
        if cid not in car_roster_map:
            car_roster_map[cid] = {
                'car_id': cid,
                'car_name': r['car_name'],
                'driver': r['driver'],
                'plate': r['plate'] or '—',
                'status': r['status'],
                'shift': r['shift'],
                'shift_zh': r['shift_zh']
            }
        else:
            # 若全日模式且夜班執勤，更新司機資訊
            if r['status'] == '執勤':
                car_roster_map[cid]['status'] = '執勤'
                car_roster_map[cid]['driver'] = r['driver']
                if r['plate']:
                    car_roster_map[cid]['plate'] = r['plate']

        if r['status'] == '執勤':
            active_cars.add(cid)

    # 2. 查詢排程站點 (依據 active_cars 與 shift)
    sched_query = f"SELECT * FROM {table_name} WHERE 1=1"
    sched_args = []
    if shift in ['day', 'night']:
        sched_query += " AND shift = ?"
        sched_args.append(shift)

    sched_rows = conn.execute(sched_query, sched_args).fetchall()

    corridor_cap_total = {}
    corridor_cap_no_u = {}
    u_boost_batches = 0

    for row in sched_rows:
        cid = row['car_id']
        # 若是全日模式，需確認該班別該車是否在勤
        if shift == 'all':
            # 檢查特定 shift 該車是否在勤
            row_shift = row['shift'].lower()
            is_active_for_shift = any(
                r['car_id'] == cid and r['shift'].lower() == row_shift and r['status'] == '執勤'
                for r in roster_rows
            )
            if not is_active_for_shift:
                continue
        else:
            if cid not in active_cars:
                continue

        flows = parse_od_pairs(dict(row))
        for (orig, dest, batches) in flows:
            k = f"{orig} ➔ {dest}"
            corridor_cap_total[k] = corridor_cap_total.get(k, 0) + batches
            if cid == 'Car_U':
                u_boost_batches += batches
            else:
                corridor_cap_no_u[k] = corridor_cap_no_u.get(k, 0) + batches

    # 3. 查詢走廊基準需求
    demands = conn.execute("SELECT from_fab, to_fab, demand_batches FROM demand_matrix WHERE demand_batches > 0").fetchall()
    conn.close()

    corridor_results = []
    overloaded_count = 0
    tight_count = 0
    normal_count = 0
    total_demand = 0
    total_capacity = sum(corridor_cap_total.values())

    for d in demands:
        orig = norm_fab(d['from_fab'])
        dest = norm_fab(d['to_fab'])
        k = f"{orig} ➔ {dest}"
        
        daily_d = d['demand_batches']
        shift_d = daily_d if shift == 'all' else round(daily_d * 0.5)
        total_demand += shift_d

        cap = corridor_cap_total.get(k, 0)
        cap_no_u = corridor_cap_no_u.get(k, 0)
        u_contrib = cap - cap_no_u

        if cap > 0:
            util = round(shift_d / cap * 100, 1)
        else:
            util = 999.9 if shift_d > 0 else 0.0

        is_over = (util > 100.0) or (shift_d > 0 and cap == 0)
        is_tight = (not is_over) and (util > 85.0)

        if is_over:
            overloaded_count += 1
            status = 'OVERLOADED'
        elif is_tight:
            tight_count += 1
            status = 'TIGHT'
        else:
            normal_count += 1
            status = 'NORMAL'

        corridor_results.append({
            'corridor': k,
            'from_fab': d['from_fab'],
            'to_fab': d['to_fab'],
            'demand': shift_d,
            'capacity': cap,
            'u_contrib': u_contrib,
            'utilization': util,
            'is_overloaded': is_over,
            'shortfall': max(0, shift_d - cap),
            'status': status
        })

    corridor_results.sort(key=lambda x: x['utilization'], reverse=True)
    
    valid_utils = [c['utilization'] for c in corridor_results if c['utilization'] < 900]
    max_util = max(valid_utils) if valid_utils else 0.0
    avg_util = round(sum(valid_utils) / len(valid_utils), 1) if valid_utils else 0.0

    return {
        'status': 'success',
        'date': date_str,
        'shift': shift,
        'table': table_name,
        'active_cars': sorted(list(active_cars)),
        'total_active_cars': len(active_cars),
        'u_car_active': ('Car_U' in active_cars),
        'u_boost_batches': u_boost_batches,
        'car_roster': car_roster_map,
        'total_demand': total_demand,
        'total_capacity': total_capacity,
        'overloaded_count': overloaded_count,
        'tight_count': tight_count,
        'normal_count': normal_count,
        'max_utilization': max_util,
        'avg_utilization': avg_util,
        'corridors': corridor_results
    }


def get_actual_cars(db_path=DB_PATH, date_str='2026-11-01', shift='all'):
    """回傳指定日期與班別下的車輛出勤名單 (包含司機與車牌，若 Car U 執勤則納入)"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cars = [dict(r) for r in conn.execute("SELECT * FROM cars ORDER BY id").fetchall()]
    
    roster_query = "SELECT * FROM driver_roster WHERE date = ?"
    args = [date_str]
    if shift in ['day', 'night']:
        roster_query += " AND lower(shift) = ?"
        args.append(shift)
        
    roster_rows = conn.execute(roster_query, args).fetchall()
    conn.close()
    
    roster_by_car = {}
    for r in roster_rows:
        cid = r['car_id']
        if cid not in roster_by_car or r['status'] == '執勤':
            roster_by_car[cid] = r
            
    res_cars = []
    for c in cars:
        cid = c['id']
        r_info = roster_by_car.get(cid)
        if r_info:
            c['driver'] = r_info['driver']
            c['plate'] = r_info['plate'] or c.get('plate', '')
            c['status'] = r_info['status']
            c['is_active'] = 1 if r_info['status'] == '執勤' else 0
        else:
            c['driver'] = '未排班'
            c['is_active'] = 0
            c['status'] = '無班次'
            
        if cid == 'Car_U':
            if c['is_active'] == 1:
                c['badge'] = '★ 夜班投入支援'
            else:
                c['badge'] = '待命備援'
        res_cars.append(c)
        
    return res_cars


def get_actual_schedules(db_path=DB_PATH, date_str='2026-11-01', shift=None, car_id=None, fab=None, mode=None, search=None, base_table='schedules'):
    """依據司機真實出勤動態生成站點排程 (包含 Car U 站點，過濾停駛車輛)"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    roster_query = "SELECT * FROM driver_roster WHERE date = ?"
    roster_rows = conn.execute(roster_query, [date_str]).fetchall()
    
    active_keys = set()
    roster_map = {}
    for r in roster_rows:
        key = (r['car_id'], r['shift'].lower())
        roster_map[key] = r
        if r['status'] == '執勤':
            active_keys.add(key)
            
    query = f"SELECT * FROM {base_table} WHERE 1=1"
    args = []
    
    if car_id and car_id != 'ALL':
        query += " AND car_id = ?"
        args.append(car_id)
        
    if shift and shift != 'all':
        query += " AND shift = ?"
        args.append(shift)
        
    if fab and fab != 'ALL':
        query += " AND fab_code = ?"
        args.append(fab)
        
    if mode and mode != 'ALL':
        query += " AND mode LIKE ?"
        args.append(f"%{mode}%")
        
    if search:
        query += " AND (cargo_cmd LIKE ? OR sop_details LIKE ? OR station_location LIKE ? OR od_flow LIKE ?)"
        term = f"%{search}%"
        args.extend([term, term, term, term])
        
    if car_id and car_id != 'ALL':
        query += ' ORDER BY CASE WHEN shift="day" THEN 0 ELSE 1 END, stop_no ASC'
    else:
        if shift == 'night':
            query += ' ORDER BY (arr_min - 1175 + 1440) % 1440 ASC'
        elif shift == 'day':
            query += ' ORDER BY arr_min ASC'
        else:
            query += ' ORDER BY (CASE WHEN shift="day" THEN arr_min WHEN shift="night" AND arr_min >= 455 THEN arr_min ELSE arr_min + 1440 END) ASC'
            
    raw_rows = conn.execute(query, args).fetchall()
    conn.close()
    
    filtered_rows = []
    for r in raw_rows:
        d = dict(r)
        cid = d['car_id']
        s_lower = d['shift'].lower()
        key = (cid, s_lower)
        
        r_info = roster_map.get(key)
        is_active = (key in active_keys)
        
        if r_info:
            d['driver_name'] = r_info['driver']
            d['plate_no'] = r_info['plate']
            d['driver_status'] = r_info['status']
            d['is_active_trip'] = 1 if is_active else 0
        else:
            d['driver_name'] = '未排班'
            d['plate_no'] = '—'
            d['driver_status'] = '無班次'
            d['is_active_trip'] = 0
            
        if (car_id and car_id != 'ALL') or is_active:
            filtered_rows.append(d)
            
    return filtered_rows


def get_actual_fab_analysis(db_path=DB_PATH, date_str='2026-11-08', fab_code='ALL', shift='all', base_table='schedules'):
    """依據指定日期的真實出勤，動態計算特定廠區或全網各廠區之班次進站與時序間隔 (包含 Car U，剔除停駛車次)"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    roster_rows = conn.execute("SELECT * FROM driver_roster WHERE date = ?", [date_str]).fetchall()
    active_shift_cars = { (r['car_id'], r['shift'].lower()) for r in roster_rows if r['status'] == '執勤' }
    roster_info = { (r['car_id'], r['shift'].lower()): r for r in roster_rows }
    
    query = f"SELECT * FROM {base_table} WHERE is_break = 0"
    args = []
    if fab_code != 'ALL':
        query += " AND fab_code = ?"
        args.append(fab_code)
    if shift != 'all':
        query += " AND shift = ?"
        args.append(shift)
        
    if shift == 'day':
        query += ' ORDER BY arr_min ASC'
    elif shift == 'night':
        query += ' ORDER BY (arr_min - 1175 + 1440) % 1440 ASC'
    else:
        query += ' ORDER BY (CASE WHEN shift="day" THEN arr_min WHEN shift="night" AND arr_min >= 455 THEN arr_min ELSE arr_min + 1440 END) ASC'
        
    raw_visits = [dict(r) for r in conn.execute(query, args).fetchall()]
    conn.close()
    
    visits = []
    for v in raw_visits:
        key = (v['car_id'], v['shift'].lower())
        if key in active_shift_cars:
            r = roster_info.get(key)
            if r:
                v['driver_name'] = r['driver']
                v['plate_no'] = r['plate']
            visits.append(v)
            
    def get_timeline_pos(v):
        if v['shift'] == 'day':
            return v['arr_min']
        return v['arr_min'] if v['arr_min'] >= 455 else v['arr_min'] + 1440

    headways = []
    for i in range(1, len(visits)):
        curr_t = get_timeline_pos(visits[i])
        prev_t = get_timeline_pos(visits[i-1])
        diff = curr_t - prev_t
        if diff >= 0:
            headways.append({
                'from_car': visits[i-1]['car_name'],
                'to_car': visits[i]['car_name'],
                'headway_min': diff,
                'time': visits[i]['arr_time']
            })
            visits[i]['headway_from_prev'] = diff
        else:
            visits[i]['headway_from_prev'] = 0

    if visits:
        visits[0]['headway_from_prev'] = 0

    avg_hw = round(sum(h['headway_min'] for h in headways) / len(headways), 1) if headways else 0
    min_hw = min((h['headway_min'] for h in headways), default=0)
    max_hw = max((h['headway_min'] for h in headways), default=0)

    cars_count = {}
    for v in visits:
        cars_count[v['car_name']] = cars_count.get(v['car_name'], 0) + 1

    mode_count = {}
    for v in visits:
        m = '專車' if '專車' in v['mode'] else ('環廠' if '環廠' in v['mode'] or '小環' in v['mode'] else '外廠/其他')
        mode_count[m] = mode_count.get(m, 0) + 1

    total_cap = sum(v['capacity_batches'] for v in visits)
    destinations = list(set(v['dest_fab'] for v in visits if v['dest_fab']))

    fleet_status = {}
    for cid in ['Car_A', 'Car_B', 'Car_C', 'Car_D', 'Car_E', 'Car_U']:
        cname = cid.replace('_', ' ')
        day_act = (cid, 'day') in active_shift_cars
        night_act = (cid, 'night') in active_shift_cars
        if shift == 'all':
            is_act = day_act or night_act
        else:
            is_act = (cid, shift.lower()) in active_shift_cars
        fleet_status[cname] = {
            'is_active': is_act,
            'day_active': day_act,
            'night_active': night_act,
            'visits_here': cars_count.get(cname, 0)
        }

    return {
        'fab_code': fab_code,
        'shift': shift,
        'date': date_str,
        'total_visits': len(visits),
        'visits': visits,
        'headways': headways,
        'avg_headway_min': avg_hw,
        'expected_wait_min': round(avg_hw / 2, 1) if avg_hw > 0 else 0,
        'min_headway_min': min_hw,
        'max_headway_min': max_hw,
        'total_capacity': total_cap,
        'cars_count': cars_count,
        'mode_count': mode_count,
        'destinations': destinations,
        'fleet_status': fleet_status
    }


def get_monthly_capacity_trend(db_path=DB_PATH, table_name='schedules'):
    """
    計算全月 (30天) 實際動態運能趨勢
    包含每日之 日運量 (Day Cap)、夜運量 (Night Cap)、24H總運量 (Total Cap) 與 基準需求量 (Demand)
    反映司機排班、請假/輪休/保養與機動車 (Car U) 支援時的實際運能波動
    """
    if table_name not in ['schedules', 'schedules_plan2', 'schedules_plan3']:
        table_name = 'schedules'

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # 1. 取得各車日/夜班額定運能
    car_shift_cap = {'day': {}, 'night': {}}
    for s in ['day', 'night']:
        rows = conn.execute(
            f"SELECT car_id, sum(capacity_batches) as cap FROM {table_name} WHERE shift = ? AND is_break = 0 GROUP BY car_id",
            [s]
        ).fetchall()
        for r in rows:
            car_shift_cap[s][r['car_id']] = r['cap']

    # 2. 需求基準 (24H 與日夜均分)
    demand_row = conn.execute("SELECT sum(demand_batches) as tot FROM demand_matrix").fetchone()
    tot_demand_24h = demand_row['tot'] if (demand_row and demand_row['tot']) else 5742
    day_demand = round(tot_demand_24h * 0.5)
    night_demand = round(tot_demand_24h * 0.5)

    # 3. 遍歷 30 天排班
    dates = [r[0] for r in conn.execute("SELECT DISTINCT date FROM driver_roster ORDER BY date").fetchall()]

    trend_details = []
    day_caps = []
    night_caps = []
    total_caps = []
    demands = []
    fulfillment_rates = []

    for d in dates:
        roster_rows = conn.execute("SELECT car_id, shift, status FROM driver_roster WHERE date = ?", [d]).fetchall()
        
        day_active = [r['car_id'] for r in roster_rows if r['shift'].lower() == 'day' and r['status'] == '執勤']
        night_active = [r['car_id'] for r in roster_rows if r['shift'].lower() == 'night' and r['status'] == '執勤']
        
        d_cap = sum(car_shift_cap['day'].get(cid, 0) for cid in day_active)
        n_cap = sum(car_shift_cap['night'].get(cid, 0) for cid in night_active)
        t_cap = d_cap + n_cap
        
        rate = round(t_cap / tot_demand_24h * 100, 1) if tot_demand_24h > 0 else 0.0
        
        day_caps.append(d_cap)
        night_caps.append(n_cap)
        total_caps.append(t_cap)
        demands.append(tot_demand_24h)
        fulfillment_rates.append(rate)

        trend_details.append({
            'date': d,
            'day_cap': d_cap,
            'night_cap': n_cap,
            'total_cap': t_cap,
            'demand': tot_demand_24h,
            'day_demand': day_demand,
            'night_demand': night_demand,
            'day_gap': d_cap - day_demand,
            'night_gap': n_cap - night_demand,
            'total_gap': t_cap - tot_demand_24h,
            'fulfillment_rate': rate,
            'day_active_count': len(day_active),
            'night_active_count': len(night_active),
            'day_active_cars': day_active,
            'night_active_cars': night_active
        })

    conn.close()

    avg_daily_cap = round(sum(total_caps) / len(total_caps), 1) if total_caps else 0
    max_daily_cap = max(total_caps) if total_caps else 0
    min_daily_cap = min(total_caps) if total_caps else 0
    avg_rate = round(sum(fulfillment_rates) / len(fulfillment_rates), 1) if fulfillment_rates else 0
    days_above = sum(1 for c in total_caps if c >= tot_demand_24h)
    days_below = sum(1 for c in total_caps if c < tot_demand_24h)

    base_caps_day = sum(car_shift_cap['day'].get(f"Car_{c}", 0) for c in ['A', 'B', 'C', 'D', 'E'])
    base_caps_night = sum(car_shift_cap['night'].get(f"Car_{c}", 0) for c in ['A', 'B', 'C', 'D', 'E'])
    baseline_cap_24h = base_caps_day + base_caps_night

    return {
        'status': 'success',
        'table': table_name,
        'total_demand_24h': tot_demand_24h,
        'day_demand': day_demand,
        'night_demand': night_demand,
        'baseline_cap_24h': baseline_cap_24h,
        'dates': dates,
        'day_caps': day_caps,
        'night_caps': night_caps,
        'total_caps': total_caps,
        'demands': demands,
        'fulfillment_rates': fulfillment_rates,
        'details': trend_details,
        'monthly_stats': {
            'avg_daily_cap': avg_daily_cap,
            'max_daily_cap': max_daily_cap,
            'min_daily_cap': min_daily_cap,
            'avg_fulfillment_rate': avg_rate,
            'days_above_demand': days_above,
            'days_below_demand': days_below
        }
    }

