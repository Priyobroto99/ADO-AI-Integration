with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

route_code = '''

@app.get("/profiles")
def get_profiles(db: Session = Depends(get_db)):
    results = db.query(models.TeamProfile, models.Team).join(models.Team).all()
    profiles = []
    for prof, team in results:
        p_dict = {k: v for k, v in prof.__dict__.items() if not k.startswith('_')}
        p_dict['engagement'] = team.engagement
        p_dict['spoc'] = team.spoc
        profiles.append(p_dict)
    return profiles

@app.get("/teams/{team_id}/profile")
def get_team_profile(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    prof = db.query(models.TeamProfile).filter(models.TeamProfile.team_id == team_id).first()
    if not prof:
        prof = models.TeamProfile(team_id=team_id, engagementCode=team.engagement)
        db.add(prof)
        db.commit()
        db.refresh(prof)
    p_dict = {k: v for k, v in prof.__dict__.items() if not k.startswith('_')}
    p_dict['engagement'] = team.engagement
    p_dict['spoc'] = team.spoc
    return p_dict

@app.put("/teams/{team_id}/profile")
def update_team_profile(team_id: int, profile_data: schemas.TeamProfileUpdate, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin", "team_spoc", "editor"]))):
    if user.role == "team_spoc" and user.team_id != team_id:
        raise HTTPException(status_code=403, detail="Not authorized to update profile for this team")
        
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
        
    prof = db.query(models.TeamProfile).filter(models.TeamProfile.team_id == team_id).first()
    if not prof:
        prof = models.TeamProfile(team_id=team_id)
        db.add(prof)
        
    for key, value in profile_data.dict(exclude_unset=True).items():
        if hasattr(prof, key):
            setattr(prof, key, value)
            
    db.commit()
    db.refresh(prof)
    return {"ok": True, "message": "Team profile updated successfully"}
'''

if '@app.get("/profiles")' not in text:
    text = text.rstrip() + route_code + '\n'
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added profile routes to backend/main.py")
else:
    print("Routes already present")
