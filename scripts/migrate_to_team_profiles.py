import sys
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
sys.path.insert(0, "backend")

from database import engine, SessionLocal, Base
from models import Team, Metric, Detail
from sqlalchemy import Column, Integer, String, Float, ForeignKey, text

# 1. Create table via raw SQL to ensure exact column specifications
create_table_sql = """
CREATE TABLE IF NOT EXISTS team_profiles (
    id SERIAL PRIMARY KEY,
    team_id INTEGER UNIQUE REFERENCES teams(id) ON DELETE CASCADE,
    
    -- General Info
    "catManager" VARCHAR,
    "engagementCode" VARCHAR,
    "lobLead" VARCHAR,
    
    -- Capability
    "cloudProf" VARCHAR,
    "cicdSetup" VARCHAR,
    "cicdMat" VARCHAR,
    "autoToolsReq" VARCHAR,
    "buildToolsReq" VARCHAR,
    "autoToolPts" VARCHAR,
    "buildToolPts" VARCHAR,
    
    -- Automation
    "autoCoverage" DOUBLE PRECISION,
    "autoStability" DOUBLE PRECISION,
    "regRunTime" DOUBLE PRECISION,
    "regExecTimeNoAuto" DOUBLE PRECISION,
    "kt" DOUBLE PRECISION,
    "ktPrep" VARCHAR,
    "assets" DOUBLE PRECISION,
    "assetPts" VARCHAR,
    "autoBugs" DOUBLE PRECISION,
    "autoBugsPts" VARCHAR,
    
    -- Program Health
    "defectLeakage" DOUBLE PRECISION,
    "prodIncidents" DOUBLE PRECISION,
    "openRisks" DOUBLE PRECISION,
    "sowMilestones" VARCHAR,
    "escalations" DOUBLE PRECISION,
    "defectPts" VARCHAR,
    "incidentPts" VARCHAR,
    "riskPts" VARCHAR,
    "sowPts" VARCHAR,
    "escalationPts" VARCHAR
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.commit()
    print("Table 'team_profiles' created/verified.")

# 2. Populate team_profiles from existing metrics & details
db = SessionLocal()
teams = db.query(Team).all()
print(f"Migrating profiles for {len(teams)} teams...")

for t in teams:
    # Find all metrics and details for this team
    metrics = db.query(Metric).filter(Metric.team_id == t.id).order_by(Metric.id.desc()).all()
    details = db.query(Detail).filter(Detail.team_id == t.id).order_by(Detail.id.desc()).all()
    
    # Helper to find first non-null across records
    def find_val(records, attr):
        for r in records:
            v = getattr(r, attr, None)
            if v is not None and v != "":
                return v
        return None

    profile_data = {
        "team_id": t.id,
        "catManager": find_val(details, "catManager"),
        "engagementCode": find_val(details, "engagementCode") or t.engagement,
        "lobLead": find_val(details, "lobLead"),
        
        "cloudProf": find_val(details, "cloudProf"),
        "cicdSetup": find_val(details, "cicdSetup"),
        "cicdMat": find_val(details, "cicdMat"),
        "autoToolsReq": find_val(metrics, "autoToolsReq"),
        "buildToolsReq": find_val(metrics, "buildToolsReq"),
        "autoToolPts": find_val(details, "autoToolPts"),
        "buildToolPts": find_val(details, "buildToolPts"),
        
        "autoCoverage": find_val(metrics, "autoCoverage"),
        "autoStability": find_val(metrics, "autoStability"),
        "regRunTime": find_val(metrics, "regRunTime"),
        "regExecTimeNoAuto": find_val(metrics, "regExecTimeNoAuto"),
        "kt": find_val(metrics, "kt"),
        "ktPrep": find_val(details, "ktPrep"),
        "assets": find_val(metrics, "assets"),
        "assetPts": find_val(details, "assetPts"),
        "autoBugs": find_val(metrics, "autoBugs"),
        "autoBugsPts": find_val(details, "autoBugsPts"),
        
        "defectLeakage": find_val(metrics, "defectLeakage"),
        "prodIncidents": find_val(metrics, "prodIncidents"),
        "openRisks": find_val(metrics, "openRisks"),
        "sowMilestones": find_val(metrics, "sowMilestones"),
        "escalations": find_val(metrics, "escalations"),
        "defectPts": find_val(details, "defectPts"),
        "incidentPts": find_val(details, "incidentPts"),
        "riskPts": find_val(details, "riskPts"),
        "sowPts": find_val(details, "sowPts"),
        "escalationPts": find_val(details, "escalationPts")
    }

    # Upsert into team_profiles
    cols = list(profile_data.keys())
    placeholders = [f":{c}" for c in cols]
    update_clause = ", ".join([f'"{c}" = EXCLUDED."{c}"' for c in cols if c != "team_id"])
    
    insert_sql = f"""
    INSERT INTO team_profiles ({', '.join([f'"{c}"' for c in cols])})
    VALUES ({', '.join(placeholders)})
    ON CONFLICT (team_id) DO UPDATE SET
    {update_clause}
    """
    
    with engine.connect() as conn:
        conn.execute(text(insert_sql), profile_data)
        conn.commit()

print(f"Successfully migrated/upserted team_profiles for all {len(teams)} teams.")
db.close()
