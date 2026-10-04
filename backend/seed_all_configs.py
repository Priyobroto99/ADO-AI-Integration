from database import engine, SessionLocal
import models

db = SessionLocal()

teams = db.query(models.Team).all()
count = 0

for team in teams:
    existing = db.query(models.TeamConfig).filter(models.TeamConfig.team_id == team.id).first()
    if not existing:
        db_cfg = models.TeamConfig(team_id=team.id)
        db.add(db_cfg)
        count += 1

db.commit()
db.close()
print(f'Successfully created team configs for {count} teams.')
