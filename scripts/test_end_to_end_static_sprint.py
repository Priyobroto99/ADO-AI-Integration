import requests

BASE_URL = "http://localhost:8000"

# 1. Fetch profiles
res = requests.get(f"{BASE_URL}/profiles")
assert res.status_code == 200, f"Failed /profiles: {res.status_code}"
profiles = res.json()
print(f"Total profiles: {len(profiles)}")

# 2. Fetch Team 11 profile
res = requests.get(f"{BASE_URL}/teams/11/profile")
assert res.status_code == 200, f"Failed team 11 profile: {res.status_code}"
prof11 = res.json()
print("Team 11 Profile:", prof11["engagement"], "| Cat Manager:", prof11["catManager"], "| Auto Coverage:", prof11["autoCoverage"])

# 3. Fetch Sprints
res = requests.get(f"{BASE_URL}/sprints")
assert res.status_code == 200
sprints = res.json()
print(f"Total sprints: {len(sprints)}")

# 4. Fetch Details
res = requests.get(f"{BASE_URL}/details")
assert res.status_code == 200
details = res.json()
sprint3_detail = next((d for d in details if d["team_id"] == 11 and d.get("sprint_id") == 3), None)
assert sprint3_detail is not None, "Team 11 Sprint 3 detail not found"
print("Team 11 Sprint 3 Stories JSON Length:", len(sprint3_detail["usAssignedPts"]))

print("\nALL BACKEND & STATIC/SPRINT CHECKS PASSED SUCCESSFULLY!")
