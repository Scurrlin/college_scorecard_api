import os
import sqlite3
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API = "https://api.data.gov/ed/collegescorecard/v1/schools"
API_KEY = os.getenv("SCORECARD_API_KEY")
UNITIDS = [164748, 192110, 167057, 192712, 211893]
YEARS = list(range(2012, 2022 + 1))

NAME_MAP = {
    164748: "Berklee College of Music",
    192110: "The Juilliard School",
    167057: "New England Conservatory",
    192712: "Manhattan School of Music",
    211893: "Curtis Institute of Music",
}

FIELD_MAP = {
    "enrollment_total": "student.size",
    "admission_rate": "admissions.admission_rate.overall",
    "retention_rate_ft": "student.retention_rate.four_year.full_time",
    "grad_rate_150": "completion.completion_rate_4yr_150nt",
    "tuition_fees": "cost.tuition.in_state",
    "avg_net_price": "cost.avg_net_price.private",
}

def create_database(db_path="music_schools.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schools (
            school_id INTEGER PRIMARY KEY AUTOINCREMENT,
            unitid INTEGER UNIQUE NOT NULL,
            institution_name TEXT NOT NULL)
    """)
    
    year_columns = [f'"{year}" REAL' for year in YEARS]

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS school_metrics_long (
            school_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            enrollment_total INTEGER,
            admission_rate REAL,
            retention_rate_ft REAL,
            grad_rate_150 REAL,
            tuition_fees REAL,
            avg_net_price REAL,
            PRIMARY KEY (school_id, year),
            FOREIGN KEY (school_id) REFERENCES schools(school_id))
    """)
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS school_metrics_wide (
            school_id INTEGER NOT NULL,
            metric_name TEXT NOT NULL,
            {', '.join(year_columns)},
            PRIMARY KEY (school_id, metric_name),
            FOREIGN KEY (school_id) REFERENCES schools(school_id))
    """)
    
    conn.commit()
    return conn

def insert_schools(conn):
    cursor = conn.cursor()
    
    for unitid, name in NAME_MAP.items():
        cursor.execute("""
            INSERT OR IGNORE INTO schools (unitid, institution_name)
            VALUES (?, ?)""", (unitid, name))
        
        cursor.execute("SELECT school_id FROM schools WHERE unitid = ?", (unitid,))
        school_id = cursor.fetchone()[0]
        
        for metric_name in FIELD_MAP.keys():
            cursor.execute("""
                INSERT OR IGNORE INTO school_metrics_wide 
                (school_id, metric_name)
                VALUES (?, ?)""", (school_id, metric_name))
    
    conn.commit()

def get_school_id(conn, unitid):
    cursor = conn.cursor()
    cursor.execute("SELECT school_id FROM schools WHERE unitid = ?", (unitid,))
    result = cursor.fetchone()
    return result[0] if result else None

def fetch_year(institution_ids, year):
    fields = ["id", "school.name"]
    fields += [f"{year}.{f}" for f in FIELD_MAP.values()]
    params = {
        "api_key": API_KEY,
        "id__in": ",".join(map(str, institution_ids)),
        "fields": ",".join(fields),
        "per_page": 100
    }
    
    try:
        r = requests.get(API, params=params, timeout=30)
        r.raise_for_status()
        js = r.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for year {year}: {e}")
        return pd.DataFrame()
    except ValueError as e:
        print(f"Error parsing JSON response for year {year}: {e}")
        return pd.DataFrame()
    
    results = js.get("results", [])
    if not results:
        print(f"Warning: No data returned for year {year}")
        return pd.DataFrame()
    
    rows = []
    for item in results:
        rid = item.get("id")
        if not rid:
            continue
            
        row = {
            "institution": NAME_MAP.get(rid, item.get("school.name", "Unknown")),
            "unitid": rid,
            "year": year,
        }

        for metric, field_suffix in FIELD_MAP.items():
            row[metric] = item.get(f"{year}.{field_suffix}")
        rows.append(row)
    return pd.DataFrame(rows)

def process_percentage_fields(df):
    percentage_fields = ["admission_rate", "retention_rate_ft", "grad_rate_150"]
    for c in percentage_fields:
        if c in df.columns:
            s = pd.to_numeric(df[c], errors="coerce")
            if s.notna().any():
                valid_values = s[s.notna()]
                if len(valid_values) > 0 and valid_values.max() <= 1.0 and valid_values.min() >= 0:
                    # Convert to percentage and round to 2 decimal places
                    df[c] = (s * 100).round(2)
                else:
                    # If already in percentage format, just round to 2 decimal places
                    df[c] = s.round(2)
    return df

def create_long_table_data(conn, df):
    cursor = conn.cursor()
    
    # Add school_id to dataframe for sorting
    df['school_id'] = df['unitid'].map(lambda x: get_school_id(conn, x))
    df_sorted = df.sort_values(['school_id', 'year'])
    
    for _, row in df_sorted.iterrows():
        school_id = row['school_id']
        if not school_id:
            continue
            
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO school_metrics_long 
                (school_id, year, enrollment_total, admission_rate, retention_rate_ft,
                 grad_rate_150, tuition_fees, avg_net_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                school_id,
                row['year'],
                row.get('enrollment_total'),
                row.get('admission_rate'),
                row.get('retention_rate_ft'),
                row.get('grad_rate_150'),
                row.get('tuition_fees'),
                row.get('avg_net_price')
            ))
        except sqlite3.Error as e:
            print(f"Error inserting long data for school_id {school_id}, year {row['year']}: {e}")
    
    conn.commit()

def create_wide_table_data(conn, df, year):
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        school_id = get_school_id(conn, row['unitid'])
        if not school_id:
            continue
        
        for metric_name in FIELD_MAP.keys():
            metric_value = row.get(metric_name)
            try:
                cursor.execute(f"""
                    UPDATE school_metrics_wide 
                    SET "{year}" = ?
                    WHERE school_id = ? AND metric_name = ?
                """, (metric_value, school_id, metric_name))
            except sqlite3.Error as e:
                print(f"Error updating {metric_name} for school_id {school_id}, year {year}: {e}")
    
    conn.commit()

def main():
    print("Creating Database...")
    print("="*60)

    db_path = f"music_schools_{datetime.now().strftime('%Y%m%d')}.db"
    conn = create_database(db_path)
    insert_schools(conn)
    failed_years = []
    all_data = []
    
    for year in YEARS:
        print(f"\nFetching data for {year}...")
        df = fetch_year(UNITIDS, year)
        
        if not df.empty:
            df = process_percentage_fields(df)
            all_data.append(df)
            create_wide_table_data(conn, df, year)
        else:
            failed_years.append(year)
            print(f"  No data available for {year}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        create_long_table_data(conn, combined_df)
    
    if failed_years:
        print(f"\nWarning: Failed to retrieve data for years: {failed_years}")
    
    conn.close()
    print(f"\nDatabase saved as: {db_path}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)