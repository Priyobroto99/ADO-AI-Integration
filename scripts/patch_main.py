import re

with open('backend/main.py', 'r') as f:
    code = f.read()

# Update configs endpoints roles
code = code.replace('auth.require_role(["admin", "editor"])', 'auth.require_role(["admin"])')

# Add endpoints
new_endpoints = '''
@app.get("/users/me", response_model=schemas.UserResponse)
def get_current_user_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.put("/metrics/{team_id}")
def update_metrics(team_id: int, metric_data: schemas.MetricBase, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin", "team_spoc", "editor"]))):
    db_metric = db.query(models.Metric).filter(models.Metric.team_id == team_id).first()
    if not db_metric:
        db_metric = models.Metric(team_id=team_id)
        db.add(db_metric)
        
    for key, value in metric_data.dict(exclude_unset=True).items():
        if key not in ['engagement', 'spoc']:
            setattr(db_metric, key, value)
            
    db.commit()
    return {"ok": True}

@app.put("/details/{team_id}")
def update_details(team_id: int, detail_data: schemas.DetailBase, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin", "team_spoc", "editor"]))):
    db_detail = db.query(models.Detail).filter(models.Detail.team_id == team_id).first()
    if not db_detail:
        db_detail = models.Detail(team_id=team_id)
        db.add(db_detail)
        
    for key, value in detail_data.dict(exclude_unset=True).items():
        if key not in ['engagement', 'spoc']:
            setattr(db_detail, key, value)
            
    db.commit()
    return {"ok": True}
'''

with open('backend/main.py', 'w') as f:
    f.write(code + '\n' + new_endpoints)
