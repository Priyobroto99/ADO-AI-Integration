import os
import pandas as pd
from database import SessionLocal, engine
import models
from sqlalchemy.orm import Session
import math

def import_data(file_path):
    df_metrics_raw = pd.read_excel(file_path, sheet_name='CAT Metrics', header=None)
    
    headers_metrics = df_metrics_raw.iloc[2].astype(str).str.lower().str.split('\n').str[0].str.strip()
    df_metrics = pd.read_excel(file_path, sheet_name='CAT Metrics', header=2)
    df_metrics.columns = headers_metrics
    
    df_details_raw = pd.read_excel(file_path, sheet_name='CAT Details', header=None)
    headers_details = df_details_raw.iloc[2].astype(str).str.lower().str.split('\n').str[0].str.strip()
    df_details = pd.read_excel(file_path, sheet_name='CAT Details', header=2)
    df_details.columns = headers_details
    
    total_teams = 26
    
    db: Session = SessionLocal()
    
    # Clear existing metrics and details
    db.query(models.Metric).delete()
    
    db.query(models.TeamConfig).delete()
    db.query(models.Team).delete()
    
    
    def get_val(row, key_contains):
        for col in row.index:
            if key_contains.lower() in str(col).lower():
                val = row[col]
                if pd.isna(val) or val == '' or val == ' ': return None
                return float(val) if isinstance(val, (int, float)) else None
        return None
        
    for i in range(total_teams):
        if i >= len(df_metrics): break
        row_m = df_metrics.iloc[i]
        engagement = row_m.iloc[0]
        spoc = row_m.iloc[1]
        
        if pd.isna(engagement) or pd.isna(spoc) or str(spoc).strip() == '' or len(str(spoc)) < 3:
            continue
            
        team = db.query(models.Team).filter(models.Team.engagement == str(engagement)).first()
        if not team:
            team = models.Team(engagement=str(engagement), spoc=str(spoc))
            db.add(team)
            db.commit()
            db.refresh(team)
            
        metric = models.Metric(
            team_id=team.id,
            spAssigned=get_val(row_m, "story points assigned"),
            spCompleted=get_val(row_m, "story points completed"),
            usAssigned=get_val(row_m, "no of user stories/tasks assigned"),
            usCompleted=get_val(row_m, "no of user stories/tasks completed"),
            usPushed=get_val(row_m, "pushed to next sprint"),
            defectLeakage=get_val(row_m, "defect leakage"),
            prodIncidents=get_val(row_m, "production incidents"),
            openRisks=get_val(row_m, "open risks & issues"),
            sowMilestones=get_val(row_m, "sow milestones"),
            escalations=get_val(row_m, "escalations"),
            autoToolsReq=get_val(row_m, "automation tool proficiencies"),
            buildToolsReq=get_val(row_m, "build tool proficiencies"),
            autoCoverage=get_val(row_m, "automation coverage"),
            autoStability=get_val(row_m, "automation stability"),
            regRunTime=get_val(row_m, "regression run time"),
            regExecTimeNoAuto=get_val(row_m, "execution time"),
            autoBugs=get_val(row_m, "automation bugs reported"),
            kt=get_val(row_m, "knowledge transfer"),
            assets=get_val(row_m, "reusable assets")
        )
        db.add(metric)
        
    for i in range(total_teams):
        if i >= len(df_details): break
        row_d = df_details.iloc[i]
        engagement = row_d.iloc[0]
        spoc = row_d.iloc[1]
        
        if pd.isna(engagement) or pd.isna(spoc) or str(spoc).strip() == '' or len(str(spoc)) < 3:
            continue
            
        def get_val_d(row, key_contains):
            for col in row.index:
                if key_contains.lower() in str(col).lower():
                    val = row[col]
                    if pd.isna(val): return None
                    return str(val)
            return None
            
        deloitteTime = get_val_d(row_d, "deloitte timesheet")
        tenroxTime = get_val_d(row_d, "tenrox timesheet")
        
        total_checks = 0
        yes_count = 0
        
        d_val = str(deloitteTime).lower().strip() if deloitteTime else ''
        t_val = str(tenroxTime).lower().strip() if tenroxTime else ''
        
        if d_val not in ('na', 'n/a', '', 'none'):
            total_checks += 1
            if d_val == 'yes': yes_count += 1
        if t_val not in ('na', 'n/a', '', 'none'):
            total_checks += 1
            if t_val == 'yes': yes_count += 1
            
        process_comp = (yes_count / total_checks * 100) if total_checks > 0 else None
        
        team = db.query(models.Team).filter(models.Team.engagement == str(engagement)).first()
        if not team:
            team = models.Team(engagement=str(engagement), spoc=str(spoc))
            db.add(team)
            db.commit()
            db.refresh(team)

        detail = models.Detail(
            team_id=team.id,
            usAssignedPts=get_val_d(row_d, "user stories/tasks assigned"),
            defectPts=get_val_d(row_d, "defect leakages"),
            incidentPts=get_val_d(row_d, "production incidents"),
            riskPts=get_val_d(row_d, "open risks"),
            sowPts=get_val_d(row_d, "sow milestones"),
            escalationPts=get_val_d(row_d, "escalations rca"),
            autoToolPts=get_val_d(row_d, "automation tool"),
            buildToolPts=get_val_d(row_d, "build tool"),
            cloudProf=get_val_d(row_d, "cloud & devops"),
            cicdSetup=get_val_d(row_d, "pipeline setup"),
            ktPrep=get_val_d(row_d, "knowledge transfer"),
            autoBugsPts=get_val_d(row_d, "automation bugs"),
            cicdMat=get_val_d(row_d, "ci/cd maturity"),
            assetPts=get_val_d(row_d, "assets reused"),
            deloitteTime=deloitteTime,
            tenroxTime=tenroxTime,
            catManager=get_val_d(row_d, "cat manager"),
            engagementCode=get_val_d(row_d, "engagement code"),
            lobLead=get_val_d(row_d, "lob lead"),
            processComp=process_comp
        )
        db.add(detail)
        
    db.commit()
    db.close()
    print("Excel data imported successfully.")

if __name__ == "__main__":
    import_data('cat_delivery_tracker.xlsx')



