from database import engine, SessionLocal
import models
from sqlalchemy import text

db = SessionLocal()
db.execute(text('DROP SCHEMA public CASCADE;'))
db.execute(text('CREATE SCHEMA public;'))
db.commit()
db.close()

models.Base.metadata.create_all(bind=engine)
print('Database wiped and completely recreated.')
