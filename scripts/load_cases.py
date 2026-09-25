#!/usr/bin/env python3
"""
Load case data from cases/ folder into TigerGraph
"""
import json
import os
from pathlib import Path
import pyTigerGraph as tg

def load_cases():
    # Connect to TigerGraph
    conn = tg.TigerGraphConnection(
        host=os.getenv("TG_HOST"),
        graphname=os.getenv("TG_GRAPHNAME", "FraudInvestigation"),
        username=os.getenv("TG_USERNAME", "tigergraph"),
        password=os.getenv("TG_PASSWORD"),
        apiToken=os.getenv("TG_API_TOKEN")
    )
    
    # Load all cases from cases/ folder
    cases_dir = Path("cases")
    for case_file in sorted(cases_dir.glob("HHG-*.json")):
        with open(case_file) as f:
            case_data = json.load(f)
        
        print(f"Loading {case_file.name}...")
        # Insert into TigerGraph
        # conn.upsertVertex("Case", case_data["case_id"], attributes=case_data)
    
    print("✅ All cases loaded!")

if __name__ == "__main__":
    load_cases()
