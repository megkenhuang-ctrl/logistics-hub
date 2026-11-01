import sqlite3
import re
import os
import json
from datetime import datetime

DB_PATH = 'logistics.db'

def clean_cell(c):
    return c.strip()

def clean_markdown_bold(s):
    return re.sub(r'[*🟦\s]', '', s).strip()

def parse_time_to_minutes(t_str):
    m = re.search(r'(\d{2}):(\d{2})', t_str)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    return None

def extract_fab_code(loc_raw):
    clean = re.sub(r'[*🟦\s]', '', loc_raw)
    if '用餐' in clean or '休息' in clean: return '休息用餐'
    if '交接' in clean: return '交接整備'
    if 'FAB8AB' in clean or '8AB' in clean: return 'FAB8AB'
    if 'FAB8CD' in clean or '8CD' in clean: return 'FAB8CD'
    if 'FAB8E' in clean or '8E' in clean: return 'FAB8E'
    if 'FAB8F' in clean or '8F' in clean: return 'FAB8F'
    if 'FAB8S' in clean or '8S' in clean: return 'FAB8S'
    if '嘉晶篤行' in clean or '篤行' in clean: return '嘉晶篤行'
    if '嘉晶創新' in clean or '創新' in clean: return '嘉晶創新'
    return 'OTHER'

def parse_mins_from_text(t_text):
    m = re.search(r'(\d+)\s*(?:mins|min|分)', t_text)
    if m:
        return int(m.group(1))
    return 0

def init_database():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create Cars table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        title TEXT NOT NULL,
        hub TEXT NOT NULL,
        phone TEXT NOT NULL,
        shift_target_cap INTEGER NOT NULL,
        description TEXT
    );
    ''')

    # 2. Create Fabs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fabs (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        display_name TEXT NOT NULL,
        color TEXT,
        description TEXT,
        demand_out_24h INTEGER DEFAULT 0,
        demand_in_24h INTEGER DEFAULT 0,
        demand_excel_sum INTEGER DEFAULT 0
    );
    ''')

    # 3. Create Schedules table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id TEXT NOT NULL,
        car_name TEXT NOT NULL,
        stop_no INTEGER NOT NULL,
        shift TEXT NOT NULL, -- 'day' or 'night'
        shift_label TEXT NOT NULL, -- '☀️ 日班' or '🌙 夜班'
        fab_code TEXT NOT NULL,
        station_raw TEXT NOT NULL,
        station_location TEXT,
        mode TEXT NOT NULL,
        od_flow TEXT NOT NULL,
        origin_fab TEXT,
        dest_fab TEXT,
        time_range TEXT NOT NULL,
        arr_time TEXT NOT NULL,
        dep_time TEXT NOT NULL,
        arr_min INTEGER NOT NULL,
        dep_min INTEGER NOT NULL,
        dwell_mins INTEGER NOT NULL,
        transit_mins INTEGER NOT NULL,
        cargo_cmd TEXT,
        sop_details TEXT,
        capacity_batches INTEGER NOT NULL,
        is_break INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(car_id) REFERENCES cars(id)
    );
    ''')

    # 4. Create Demand Matrix table (from Demand_from_to.xlsx)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS demand_matrix (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_fab TEXT NOT NULL,
        to_fab TEXT NOT NULL,
        demand_batches INTEGER NOT NULL,
        demand_shift_batches INTEGER NOT NULL
    );
    ''')

    # Insert Cars Metadata
    car_meta = [
        ('Car_A', 'Car A', '外廠門戶與全廠巡迴旗艦', 'FAB8E 1F 大廳', '8644824（0960-717239）', 360, '專車直達（晨間）+ 嘉晶外廠專營 + 環廠巡迴'),
        ('Car_B', 'Car B', 'FAB8F 代工母港主動脈專車', 'FAB8F 代工出入口', '8644828（0960-717178）', 600, '8F 十字路口超級重砲，高密度對開與午休跨休專車'),
        ('Car_C', 'Car C', 'FAB8AB 力行心臟與 8F 密集對開', 'FAB8AB 1F 大廳', '8644830（0960-717258）', 520, '力行 8AB 大廳主力與午後大環巡迴'),
        ('Car_D', 'Car D', 'FAB8CD 母港全日純環廠巡迴車', 'FAB8CD 裝卸碼頭上 3F', '8681029（0965-702916）', 240, '全廠巡迴（8CD➔8F➔8S➔8E➔8AB），主扛 8S 庫房'),
        ('Car_E', 'Car E', 'FAB8S 庫房母港專車與小環', 'FAB8S 1F 碼頭/8S5A', '8681030（0965-702918）', 480, '8S 庫房始發，日班試運行，密集庫房出入料'),
        ('Car_U', 'Car U', '聯電同仁支援加班車（專車+小環）', 'FAB8S 1F 碼頭/8S5A', '8638834（0975-612990）', 496, '專車(站次1~12) + 藍色框小環(站次13~18)，窗口：8_MIT-PTI 洪婷 8638833，車牌 RGE-2107')
    ]
    cursor.executemany('INSERT INTO cars VALUES (?,?,?,?,?,?,?)', car_meta)

    # Add plate_no column to cars
    cursor.execute("ALTER TABLE cars ADD COLUMN plate_no TEXT")
    plate_map = {
        'Car_A': 'KPC-6593', 'Car_B': 'KPC-6586', 'Car_C': 'KPC-6588',
        'Car_D': 'KPA-7309', 'Car_E': 'KPC-6131', 'Car_U': 'RGE-2107'
    }
    for cid, p in plate_map.items():
        cursor.execute("UPDATE cars SET plate_no = ? WHERE id = ?", (p, cid))

    # Insert Fabs Metadata (including Demand_from_to.xlsx 24H Outbound/Inbound OD sums & Excel Col J Sum)
    fab_meta = [
        ('FAB8AB', 'FAB8AB', '力行廠 FAB8AB (1F大廳)', '#3B82F6', '力行核心廠區，大廳平面裝卸', 450, 450, 908),
        ('FAB8CD', 'FAB8CD', '碼頭廠 FAB8CD (裝卸碼頭3F)', '#10B981', '裝卸專用碼頭，需上3F換車作業', 530, 530, 1052),
        ('FAB8E', 'FAB8E', '門戶廠 FAB8E (1F大廳)', '#8B5CF6', '外廠對接門戶，直達嘉晶外廠站點', 420, 420, 865),
        ('FAB8F', 'FAB8F', '代工廠 FAB8F (代工出入口)', '#F59E0B', '全廠代工核心樞紐，物料流量最高', 830, 830, 1662),
        ('FAB8S', 'FAB8S', '庫房廠 FAB8S (1F碼頭/8S5A)', '#EF4444', '物料儲備與大型庫房基地', 430, 430, 747),
        ('嘉晶篤行', '嘉晶篤行', '外廠 嘉晶篤行站點', '#06B6D4', '篤行外廠站點，由 Car A 獨家對開', 30, 30, 30),
        ('嘉晶創新', '嘉晶創新', '外廠 嘉晶創新站點', '#14B8A6', '創新外廠站點，由 Car A 獨家對開', 30, 30, 30)
    ]
    cursor.executemany('INSERT INTO fabs VALUES (?,?,?,?,?,?,?,?)', fab_meta)

    # Insert Demand Matrix (from Demand_from_to.xlsx - 24H Full Day Demand & 12H Shift Demand)
    demands_24h = []
    if os.path.exists('Demand_from_to.xlsx'):
        try:
            import openpyxl
            wb = openpyxl.load_workbook('Demand_from_to.xlsx', data_only=True)
            ws = wb.active
            def norm_xl_fab(val):
                if not val: return None
                s = str(val).strip()
                if 'FAB8AB' in s: return 'FAB8AB'
                if 'FAB8CD' in s: return 'FAB8CD'
                if 'FAB8E' in s: return 'FAB8E'
                if 'FAB8F' in s: return 'FAB8F'
                if 'FAB8S' in s: return 'FAB8S'
                if '篤行' in s: return '嘉晶篤行'
                if '創新' in s: return '嘉晶創新'
                return None

            col_fabs = {c: norm_xl_fab(ws.cell(2, c).value) for c in range(3, 10)}
            for r in range(3, 10):
                f_from = norm_xl_fab(ws.cell(r, 2).value)
                if not f_from: continue
                for c, f_to in col_fabs.items():
                    if not f_to or f_from == f_to: continue
                    v = ws.cell(r, c).value
                    if isinstance(v, (int, float)) and v > 0:
                        d24 = int(round(v))
                        demands_24h.append((f_from, f_to, d24, d24 // 2))
        except Exception as e:
            print(f"Warning reading Demand_from_to.xlsx via openpyxl: {e}")

    if not demands_24h:
        raw_demands = [
            ('FAB8AB', 'FAB8E', 150), ('FAB8AB', 'FAB8F', 250), ('FAB8AB', 'FAB8S', 50),
            ('FAB8CD', 'FAB8E', 150), ('FAB8CD', 'FAB8F', 300), ('FAB8CD', 'FAB8S', 80),
            ('FAB8E', 'FAB8AB', 150), ('FAB8E', 'FAB8CD', 150), ('FAB8E', 'FAB8F', 20),
            ('FAB8E', 'FAB8S', 40), ('FAB8E', '嘉晶篤行', 30), ('FAB8E', '嘉晶創新', 30),
            ('FAB8F', 'FAB8AB', 250), ('FAB8F', 'FAB8CD', 300), ('FAB8F', 'FAB8E', 20), ('FAB8F', 'FAB8S', 260),
            ('FAB8S', 'FAB8AB', 50), ('FAB8S', 'FAB8CD', 80), ('FAB8S', 'FAB8E', 40), ('FAB8S', 'FAB8F', 260),
            ('嘉晶篤行', 'FAB8E', 30), ('嘉晶創新', 'FAB8E', 30)
        ]
        demands_24h = [(o, d, v, v // 2) for (o, d, v) in raw_demands]

    cursor.executemany('INSERT INTO demand_matrix (from_fab, to_fab, demand_batches, demand_shift_batches) VALUES (?,?,?,?)', demands_24h)

    # Read Raw Data
    import make_all_cars_unified_tables as m
    
    total_stops = 0

    for car_key, rows in m.output_docs.items():
        car_id = car_key
        car_name = car_key.replace('_', ' ')
        
        for r in rows:
            cols = [clean_cell(c) for c in r.split('|')[1:-1]]
            stop_no_match = re.search(r'\d+', cols[1])
            stop_no = int(stop_no_match.group(0)) if stop_no_match else 0

            loc_raw = cols[2]
            mode = re.sub(r'[*]', '', cols[3]).strip()
            od_flow = re.sub(r'[*]', '', cols[4]).strip()
            day_t = cols[5].strip()
            night_t = cols[6].strip()
            dwell_str = cols[7].strip()
            transit_str = cols[8].strip()
            cargo_cmd = cols[9].strip()
            sop_details = cols[10].strip()

            dwell_mins = parse_mins_from_text(dwell_str)
            transit_mins = parse_mins_from_text(transit_str)

            fab_code = extract_fab_code(loc_raw)
            is_break = 1 if fab_code in ['休息用餐', '交接整備'] else 0

            # Extract location description
            parts = loc_raw.replace('**', '').replace('🟦', '').split('<br>')
            station_loc = parts[1].strip() if len(parts) > 1 else parts[0].strip()

            # Capacity estimation (Detail 1 Fix: restore 40 batches for terminal release & lunch preload)
            cap = 40 if '專車' in mode else 16
            if ('40' in cargo_cmd or '預載滿' in cargo_cmd) and '24' not in cargo_cmd:
                cap = 40
            if '24' in cargo_cmd:
                cap = 24
            if is_break or '清空' in od_flow or '卸清' in od_flow or '全卸載' in od_flow or '末班卸貨' in od_flow:
                cap = 0

            # Origin and dest fab (clean multi-line <br> tags)
            orig_fab = fab_code
            dest_fab = ''
            if '➔' in od_flow:
                first_line = od_flow.split('<br>')[0]
                if '➔' in first_line:
                    dest_fab = first_line.split('➔')[1].split('/')[0].strip()

            # Process Day Shift
            day_times = re.findall(r'\d{2}:\d{2}', day_t)
            if len(day_times) >= 2:
                day_arr, day_dep = day_times[0], day_times[1]
                day_arr_min = parse_time_to_minutes(day_arr)
                day_dep_min = parse_time_to_minutes(day_dep)
                cursor.execute('''
                INSERT INTO schedules (
                    car_id, car_name, stop_no, shift, shift_label, fab_code, station_raw, station_location,
                    mode, od_flow, origin_fab, dest_fab, time_range, arr_time, dep_time, arr_min, dep_min,
                    dwell_mins, transit_mins, cargo_cmd, sop_details, capacity_batches, is_break
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', (
                    car_id, car_name, stop_no, 'day', '☀️ 日班', fab_code, loc_raw, station_loc,
                    mode, od_flow, orig_fab, dest_fab, f'{day_arr} - {day_dep}', day_arr, day_dep, day_arr_min, day_dep_min,
                    dwell_mins, transit_mins, cargo_cmd, sop_details, cap, is_break
                ))
                total_stops += 1

            # Process Night Shift
            night_times = re.findall(r'\d{2}:\d{2}', night_t)
            if len(night_times) >= 2:
                night_arr, night_dep = night_times[0], night_times[1]
                night_arr_min = parse_time_to_minutes(night_arr)
                night_dep_min = parse_time_to_minutes(night_dep)
                cursor.execute('''
                INSERT INTO schedules (
                    car_id, car_name, stop_no, shift, shift_label, fab_code, station_raw, station_location,
                    mode, od_flow, origin_fab, dest_fab, time_range, arr_time, dep_time, arr_min, dep_min,
                    dwell_mins, transit_mins, cargo_cmd, sop_details, capacity_batches, is_break
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', (
                    car_id, car_name, stop_no, 'night', '🌙 夜班', fab_code, loc_raw, station_loc,
                    mode, od_flow, orig_fab, dest_fab, f'{night_arr} - {night_dep}', night_arr, night_dep, night_arr_min, night_dep_min,
                    dwell_mins, transit_mins, cargo_cmd, sop_details, cap, is_break
                ))
                total_stops += 1

    # Create handy indexes for rapid queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sched_car ON schedules(car_id, shift);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sched_fab ON schedules(fab_code, shift);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sched_arr ON schedules(arr_min);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sched_dep ON schedules(dep_min);')

    # 5. Create Driver Roster table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS driver_roster (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        weekday TEXT NOT NULL,
        shift TEXT NOT NULL, -- 'Day' or 'Night'
        shift_zh TEXT NOT NULL, -- '日班' or '夜班'
        car_id TEXT NOT NULL,
        car_name TEXT NOT NULL,
        plate TEXT,
        status TEXT NOT NULL, -- '執勤', '預備車', '無班次'
        driver TEXT,
        driver_type TEXT, -- '廠區正班', 'IJM外包', '預備車', '無'
        confidence REAL,
        FOREIGN KEY(car_id) REFERENCES cars(id)
    );
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_roster_date ON driver_roster(date, shift);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_roster_driver ON driver_roster(driver);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_roster_car ON driver_roster(car_id);')

    roster_file = 'driver_roster_202611.json'
    if os.path.exists(roster_file):
        with open(roster_file, 'r', encoding='utf-8') as rf:
            roster_data = json.load(rf)
        for r in roster_data:
            cursor.execute('''
            INSERT INTO driver_roster (
                date, weekday, shift, shift_zh, car_id, car_name, plate, status, driver, driver_type, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                r['date'], r['weekday'], r['shift'], r['shift_zh'], r['car_id'], r['car_name'],
                r['plate'], r['status'], r['driver'], r['driver_type'], r['confidence']
            ))
        print(f"Driver roster ({len(roster_data)} records) imported into database!")

    conn.commit()

    # Export db_export.json so offline mode stays in sync
    conn.row_factory = sqlite3.Row
    export_data = {
        'cars': [dict(r) for r in conn.execute('SELECT * FROM cars').fetchall()],
        'fabs': [dict(r) for r in conn.execute('SELECT * FROM fabs').fetchall()],
        'schedules': [dict(r) for r in conn.execute('SELECT * FROM schedules').fetchall()],
        'demand_matrix': [dict(r) for r in conn.execute('SELECT * FROM demand_matrix').fetchall()],
        'driver_roster': [dict(r) for r in conn.execute('SELECT * FROM driver_roster').fetchall()],
        'exported_at': datetime.now().isoformat()
    }
    with open('db_export.json', 'w', encoding='utf-8') as ef:
        json.dump(export_data, ef, ensure_ascii=False, indent=2)

    conn.close()

    print(f"Database {DB_PATH} and db_export.json initialized successfully!")
    print(f"Total schedule records inserted: {total_stops}")
    print(f"Total demand_matrix records inserted: {len(demands_24h)}")

if __name__ == '__main__':
    init_database()
