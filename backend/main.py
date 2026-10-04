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
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
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
    results = db.query(models.Metric, models.Team).join(models.Team).all()
    metrics = []
    for metric, team in results:
        m_dict = {k: v for k, v in metric.__dict__.items() if not k.startswith('_')}
        m_dict['engagement'] = team.engagement
        m_dict['spoc'] = team.spoc
        metrics.append(m_dict)
    return metrics

@app.get("/details", response_model=list[schemas.DetailResponse])
def get_details(db: Session = Depends(get_db)):
    results = db.query(models.Detail, models.Team).join(models.Team).all()
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
        "autoToolsReq": "lower",
        "buildToolsReq": "lower"
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
