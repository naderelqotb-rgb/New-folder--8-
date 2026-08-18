#!/usr/bin/env python3
"""Build Rasam telemetry database from raw CSV files."""

import sqlite3
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
DB_PATH = DATA_DIR / "rasam_telemetry.sqlite"


def load_csv(table_name: str) -> pd.DataFrame:
    """Load a CSV file for the given table name."""
    csv_path = RAW_DIR / f"solar_telemetry.{table_name}.csv"
    return pd.read_csv(csv_path)


def create_database():
    """Create SQLite database with 4 tables from raw CSVs."""
    tables = ["inverter_data", "lvpanel_data", "mvpanel_data", "string_data"]
    
    conn = sqlite3.connect(DB_PATH)
    
    for table in tables:
        df = load_csv(table)
        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"Created table '{table}' with {len(df)} rows")
    
    conn.close()
    print(f"\nDatabase created at: {DB_PATH}")


if __name__ == "__main__":
    create_database()
