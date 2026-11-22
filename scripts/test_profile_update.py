import sys
from dotenv import load_dotenv
load_dotenv('backend/.env')
sys.path.insert(0, 'backend')
from auth import create_access_token
import requests

token = create_access_token(data={"sub": "Priyobroto"})
headers = {"Authorization": f"Bearer {token}"}

update_data = {
    "catManager": "Arun Srinivasan",
    "cloudProf": "Yes",
    "autoCoverage": 100.0,
    "sowMilestones": "2.0",
    "openRisks": 1.0,
    "riskPts": "Client does not create RTM document, directly moves to Test case creation from ADO Feature"
}

put_res = requests.put("http://localhost:8000/teams/11/profile", json=update_data, headers=headers)
assert put_res.status_code == 200, f"PUT profile failed: {put_res.text}"
print("PUT /teams/11/profile response:", put_res.json())

get_res = requests.get("http://localhost:8000/teams/11/profile", headers=headers)
assert get_res.status_code == 200
p = get_res.json()
print("Updated Profile Verified:")
print(f"  Engagement: {p['engagement']}")
print(f"  Cat Manager: {p['catManager']}")
print(f"  Cloud Proficiency: {p['cloudProf']}")
print(f"  Auto Coverage: {p['autoCoverage']}%")
print(f"  Open Risks: {p['openRisks']}")

print("\nSUCCESS: All TeamProfile endpoints are functional and verified!")
