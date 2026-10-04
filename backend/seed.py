from database import SessionLocal
import models, auth

db = SessionLocal()

# Check and add admin
admin_user = db.query(models.User).filter(models.User.username == 'admin').first()
if not admin_user:
    hashed_password = auth.get_password_hash('admin123')
    admin_user = models.User(username='admin', hashed_password=hashed_password, role='admin')
    db.add(admin_user)

# Check and add team_spoc
spoc_user = db.query(models.User).filter(models.User.username == 'spoc').first()
if not spoc_user:
    hashed_password = auth.get_password_hash('spoc123')
    spoc_user = models.User(username='spoc', hashed_password=hashed_password, role='team_spoc')
    db.add(spoc_user)

db.commit()
db.close()
print("Database seeded with users.")
