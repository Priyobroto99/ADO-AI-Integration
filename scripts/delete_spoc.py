import os
import sys

# Ensure backend directory is in path and load environment
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_root, "backend")
sys.path.append(backend_dir)

from dotenv import load_dotenv
load_dotenv(os.path.join(backend_dir, ".env"))

from database import SessionLocal
import models

def delete_spoc_user(username: str = "Priyobroto"):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            print(f"[!] User '{username}' not found in database.")
            return False

        print(f"[*] Found User:")
        print(f"    - ID: {user.id}")
        print(f"    - Username: {user.username}")
        print(f"    - Role: {user.role}")
        print(f"    - Mapped Team ID: {user.team_id}")

        if user.team_id:
            team = db.query(models.Team).filter(models.Team.id == user.team_id).first()
            if team:
                print(f"[*] Linked Team:")
                print(f"    - Team ID: {team.id}")
                print(f"    - Engagement: {team.engagement}")
                print(f"    - SPOC: {team.spoc}")

        # Delete the SPOC user
        db.delete(user)
        db.commit()
        print(f"[OK] Successfully deleted user '{username}'.")
        print(f"[OK] Team ID {user.team_id} is now unmapped and ready for fresh onboarding.")
        return True

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error during deletion: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    target_username = sys.argv[1] if len(sys.argv) > 1 else "Priyobroto"
    print(f"=== Deleting SPOC User: {target_username} ===")
    delete_spoc_user(target_username)
