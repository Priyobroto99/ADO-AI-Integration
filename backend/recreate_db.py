from database import engine, SessionLocal
import models
from sqlalchemy import text

db = SessionLocal()
db.execute(text("DROP TABLE IF EXISTS metrics CASCADE"))
db.execute(text("DROP TABLE IF EXISTS details CASCADE"))
db.execute(text('DROP TABLE IF EXISTS team_configs CASCADE'))
db.execute(text('DROP TABLE IF EXISTS teams CASCADE'))
db.commit()
db.close()

models.Base.metadata.create_all(bind=engine)
print('Tables recreated successfully.')

