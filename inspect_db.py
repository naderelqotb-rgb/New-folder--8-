#!/usr/bin/env python3
"""Inspect Rasam telemetry database (read-only)."""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "rasam_telemetry.sqlite"
TABLES = ["inverter_data", "lvpanel_data", "mvpanel_data", "string_data"]


def inspect_table(conn, table_name):
    """Inspect a single table: columns, row count, and first 3 rows."""
    cursor = conn.cursor()
    
    # Get column info
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    
    # Get first 3 rows
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 3", conn)
    
    return columns, row_count, df


def main():
    db_uri = f"file:{DB_PATH}?mode=ro"
    conn = sqlite3.connect(db_uri, uri=True)
    
    summary = []
    
    for table in TABLES:
        print(f"\n{'='*60}")
        print(f"TABLE: {table}")
        print('='*60)
        
        columns, row_count, df = inspect_table(conn, table)
        
        # Print column names and types
        print("\nColumns:")
        for col in columns:
            # col format: (cid, name, type, notnull, dflt_value, pk)
            print(f"  - {col[1]} ({col[2]})")
        
        # Print row count
        print(f"\nTotal rows: {row_count}")
        
        # Print first 3 rows
        print("\nFirst 3 rows:")
        print(df.to_string())
        
        summary.append((table, len(columns), row_count))
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    for table, col_count, row_count in summary:
        print(f"{table}: {col_count} columns, {row_count} rows")
    
    conn.close()


if __name__ == "__main__":
    main()
