
import csv
import sqlite3
import os

def save_to_csv(items, out_file, fieldnames=None):
    mode = 'w'
    os.makedirs(os.path.dirname(out_file) or '.', exist_ok=True)
    with open(out_file, mode, encoding='utf-8', newline='') as f:
        if not fieldnames:
            
            first = next(iter(items), None)
            if first is None:
                return
            fieldnames = sorted(first.keys())
            f.seek(0)
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(first)
            for it in items:
                writer.writerow(it)
            return
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for it in items:
            writer.writerow(it)

def save_to_sqlite(items, out_file, table='vacancies'):
    os.makedirs(os.path.dirname(out_file) or '.', exist_ok=True)
    conn = sqlite3.connect(out_file)
    cur = conn.cursor()
    
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table} (
        vacancy_id TEXT PRIMARY KEY,
        name TEXT,
        area TEXT,
        employer TEXT,
        published_at TEXT,
        raw_json TEXT
    )""")
    inserted = 0
    for it in items:
        vid = it.get('id')
        try:
            cur.execute(f"INSERT OR IGNORE INTO {table} (vacancy_id,name,area,employer,published_at,raw_json) VALUES (?,?,?,?,?,?)",
                        (vid, it.get('name'), 
                         str(it.get('area',{}).get('name')), 
                         str(it.get('employer',{}).get('name')), 
                         it.get('published_at'), 
                         str(it)))
            inserted += cur.rowcount
        except Exception as e:
           
            continue
    conn.commit()
    conn.close()
    return inserted
