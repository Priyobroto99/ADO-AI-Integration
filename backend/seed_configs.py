from database import engine, SessionLocal
import models

db = SessionLocal()

default_team = db.query(models.Team).filter(models.Team.engagement == 'Default').first()
if not default_team:
    default_team = models.Team(engagement='Default', spoc='System')
    db.add(default_team)
    db.commit()
    db.refresh(default_team)

existing = db.query(models.TeamConfig).filter(models.TeamConfig.team_id == default_team.id).first()
if not existing:
    db_cfg = models.TeamConfig(team_id=default_team.id)
    db.add(db_cfg)
else:
    # already there, just rely on defaults for now
    pass
    
db.commit()
db.close()
print('Default configs seeded (wide format).')
