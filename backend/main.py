from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas, auth
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ADO Integration API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    team_id = user.team_id
    if user.role == "team_spoc":
        if team_id:
            # Check if a SPOC already exists for this team
            existing_spoc = db.query(models.User).filter(
                models.User.team_id == team_id, 
                models.User.role == "team_spoc"
            ).first()
            if existing_spoc:
                raise HTTPException(
                    status_code=400, 
                    detail="spoc already exists please ask admin to remove existing spoc before mapping new spoc to team"
                )
        elif user.new_team_name:
            # Check if engagement already exists
            existing_team = db.query(models.Team).filter(models.Team.engagement == user.new_team_name).first()
            if existing_team:
                raise HTTPException(status_code=400, detail="Team/Engagement already exists. Please select it from the list.")
            
            # Create the team
            new_team = models.Team(engagement=user.new_team_name, spoc=user.username)
            db.add(new_team)
            db.commit()
            db.refresh(new_team)
            team_id = new_team.id
        else:
            raise HTTPException(status_code=400, detail="Must provide either team_id or new_team_name for a SPOC")

    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username, 
        hashed_password=hashed_password, 
        role=user.role,
        team_id=team_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/metrics", response_model=list[schemas.MetricResponse])
def get_metrics(db: Session = Depends(get_db)):
    results = db.query(models.Metric, models.Team).join(models.Team).order_by(models.Metric.id.desc()).all()
    metrics = []
    for metric, team in results:
        m_dict = {k: v for k, v in metric.__dict__.items() if not k.startswith('_')}
        m_dict['engagement'] = team.engagement
        m_dict['spoc'] = team.spoc
        metrics.append(m_dict)
    return metrics

@app.get("/details", response_model=list[schemas.DetailResponse])
def get_details(db: Session = Depends(get_db)):
    results = db.query(models.Detail, models.Team).join(models.Team).order_by(models.Detail.id.desc()).all()
    details = []
    for detail, team in results:
        d_dict = {k: v for k, v in detail.__dict__.items() if not k.startswith('_')}
        d_dict['engagement'] = team.engagement
        d_dict['spoc'] = team.spoc
        details.append(d_dict)
    return details

@app.get("/teams", response_model=list[schemas.TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    return db.query(models.Team).all()

@app.post("/teams", response_model=schemas.TeamResponse)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin"]))):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@app.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin"]))):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Cascade delete if required, here manual
    db.query(models.Metric).filter(models.Metric.team_id == team_id).delete()
    db.query(models.Detail).filter(models.Detail.team_id == team_id).delete()
    db.query(models.TeamConfig).filter(models.TeamConfig.team_id == team_id).delete()
    db.delete(team)
    db.commit()
    return {"ok": True}

@app.get("/configs")
def get_configs(db: Session = Depends(get_db)):
    configs = db.query(models.TeamConfig, models.Team).join(models.Team).all()
    
    # Types map
    types_map = {
        "spAssigned": "higher",
        "spCompleted": "higher",
        "usPushed": "lower",
        "defectLeakage": "lower",
        "prodIncidents": "lower",
        "openRisks": "lower",
        "escalations": "lower",
        "autoCoverage": "higher",
        "autoStability": "higher",
        "autoToolsReq": "higher",
        "buildToolsReq": "higher"
    }
    
    result = {"Default": {}}
    for config, team in configs:
        if team.engagement not in result:
            result[team.engagement] = {}
            
        for metric, m_type in types_map.items():
            result[team.engagement][metric] = {
                "expected": getattr(config, f"{metric}_expected", None),
                "variance": getattr(config, f"{metric}_variance", None),
                "type": m_type
            }
            
    return result

@app.post("/teams/{team_id}/configs", response_model=schemas.TeamConfigResponse)
def create_team_config(team_id: int, config: schemas.TeamConfigCreate, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin"]))):
    db_config = db.query(models.TeamConfig).filter(models.TeamConfig.team_id == team_id).first()
    if db_config:
        raise HTTPException(status_code=400, detail="Config already exists for this team")
    db_config = models.TeamConfig(team_id=team_id, **config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@app.put("/teams/{team_id}/configs")
def update_team_config(team_id: int, config: schemas.TeamConfigCreate, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin"]))):
    db_config = db.query(models.TeamConfig).filter(models.TeamConfig.team_id == team_id).first()
    if not db_config:
        db_config = models.TeamConfig(team_id=team_id)
        db.add(db_config)
    
    for key, value in config.dict().items():
        setattr(db_config, key, value)
        
    db.commit()
    return {"ok": True}


@app.get("/users/me", response_model=schemas.UserResponse)
def get_current_user_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

from ado_client import ADOClient

@app.get("/sprints", response_model=list[schemas.SprintResponse])
def get_sprints(db: Session = Depends(get_db)):
    return db.query(models.Sprint).all()

@app.post("/sprints", response_model=schemas.SprintResponse)
def create_sprint(sprint_data: schemas.SprintCreate, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin", "team_spoc", "editor"]))):
    existing = db.query(models.Sprint).filter(models.Sprint.name == sprint_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Sprint with this name already exists")
    new_sprint = models.Sprint(
        name=sprint_data.name,
        start_date=sprint_data.start_date,
        end_date=sprint_data.end_date
    )
    db.add(new_sprint)
    db.commit()
    db.refresh(new_sprint)
    return new_sprint

@app.put("/teams/{team_id}/ado-config")
def update_ado_config(team_id: int, ado_config: schemas.ADOConfigUpdate, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin", "team_spoc", "editor"]))):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
        
    if user.role == "team_spoc" and user.team_id != team_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    if ado_config.ado_org is not None:
        team.ado_org = ado_config.ado_org
    if ado_config.ado_project is not None:
        team.ado_project = ado_config.ado_project
    if ado_config.ado_team is not None:
        team.ado_team = ado_config.ado_team
    if ado_config.ado_pat is not None:
        team.ado_pat = ado_config.ado_pat
    if ado_config.ado_iteration is not None:
        team.ado_iteration = ado_config.ado_iteration
        
    db.commit()
    return {"message": "ADO Config updated"}

@app.get("/teams/{team_id}/ado-preview")
def ado_preview(team_id: int, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin", "team_spoc", "editor"]))):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
        
    if user.role == "team_spoc" and user.team_id != team_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    if not team.ado_org or not team.ado_project or not team.ado_pat or not team.ado_team:
        raise HTTPException(status_code=400, detail="Incomplete ADO configuration for this team. Please configure ADO Settings first.")
        
    client = ADOClient(team.ado_org, team.ado_project, team.ado_pat, team.ado_team)
    try:
        preview_data = client.preview_sync(team.ado_iteration)
        return preview_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/metrics/{team_id}")
def update_metrics(team_id: int, metric_data: schemas.MetricBase, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin", "team_spoc", "editor"]))):
    if user.role == "team_spoc" and user.team_id != team_id:
        raise HTTPException(status_code=403, detail="Not authorized to update metrics for this team")

    sprint_id = metric_data.sprint_id
    if not sprint_id:
        raise HTTPException(status_code=400, detail="sprint_id is required")

    db_metric = db.query(models.Metric).filter(models.Metric.team_id == team_id, models.Metric.sprint_id == sprint_id).first()
    if not db_metric:
        db_metric = models.Metric(team_id=team_id, sprint_id=sprint_id, sprint=metric_data.sprint)
        db.add(db_metric)
        
    for key, value in metric_data.dict(exclude_unset=True).items():
        if key not in ['engagement', 'spoc', 'sprint_id']:
            setattr(db_metric, key, value)
            
    db.commit()
    return {"ok": True}

@app.put("/details/{team_id}")
def update_details(team_id: int, detail_data: schemas.DetailBase, db: Session = Depends(get_db), user: models.User = Depends(auth.require_role(["admin", "team_spoc", "editor"]))):
    if user.role == "team_spoc" and user.team_id != team_id:
        raise HTTPException(status_code=403, detail="Not authorized to update details for this team")

    sprint_id = detail_data.sprint_id
    if not sprint_id:
        raise HTTPException(status_code=400, detail="sprint_id is required")

    db_detail = db.query(models.Detail).filter(models.Detail.team_id == team_id, models.Detail.sprint_id == sprint_id).first()
    if not db_detail:
        db_detail = models.Detail(team_id=team_id, sprint_id=sprint_id, sprint=detail_data.sprint)
        db.add(db_detail)
        
    for key, value in detail_data.dict(exclude_unset=True).items():
        if key not in ['engagement', 'spoc', 'sprint_id']:
            setattr(db_detail, key, value)
            
    db.commit()
    return {"ok": True}
