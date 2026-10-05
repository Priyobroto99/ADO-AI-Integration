import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

class ADOClient:
    def __init__(self, org, project, pat, team):
        self.org = org
        self.project = project
        self.pat = pat
        self.team = team
        self.base_url = f"https://dev.azure.com/{org}/{project}"

    def get_current_iteration(self):
        # Calls the Azure DevOps iterations API
        url = f"{self.base_url}/{self.team}/_apis/work/teamsettings/iterations?api-version=6.0&$timeframe=current"
        response = requests.get(url, auth=HTTPBasicAuth("", self.pat))
        if response.status_code != 200:
            raise Exception(f"Failed to fetch current iteration: {response.text}")
        data = response.json()
        if data.get("count", 0) == 0:
            raise Exception("No active iteration found.")
        return data["value"][0] # Returns the first current iteration

    def get_iteration_work_items(self, iteration_path):
        # Use WIQL to get work items for the iteration
        url = f"https://dev.azure.com/{self.org}/{self.project}/_apis/wit/wiql?api-version=6.0"
        
        query = f"""
        SELECT [System.Id], [System.Title], [System.State], [Microsoft.VSTS.Scheduling.StoryPoints]
        FROM workitems
        WHERE [System.TeamProject] = '{self.project}'
        AND [System.IterationPath] = '{iteration_path}'
        AND [System.WorkItemType] IN ('User Story', 'Bug')
        """
        response = requests.post(url, auth=HTTPBasicAuth("", self.pat), json={"query": query})
        if response.status_code != 200:
            raise Exception(f"Failed to execute WIQL: {response.text}")
        
        data = response.json()
        work_item_relations = data.get("workItems", [])
        if not work_item_relations:
            return []

        # Get details for these work items (including Title)
        ids = [str(item["id"]) for item in work_item_relations]
        ids_str = ",".join(ids)
        fields = "System.Id,System.Title,System.State,System.WorkItemType,Microsoft.VSTS.Scheduling.StoryPoints"
        details_url = (
            f"https://dev.azure.com/{self.org}/{self.project}/_apis/wit/workitems"
            f"?ids={ids_str}&fields={fields}&api-version=6.0"
        )
        
        details_res = requests.get(details_url, auth=HTTPBasicAuth("", self.pat))
        if details_res.status_code != 200:
            raise Exception(f"Failed to fetch work item details: {details_res.text}")
            
        return details_res.json().get("value", [])

    def get_iteration_by_name(self, iteration_name: str):
        url = f"{self.base_url}/{self.team}/_apis/work/teamsettings/iterations?api-version=6.0"
        response = requests.get(url, auth=HTTPBasicAuth("", self.pat))
        if response.status_code != 200:
            raise Exception(f"Failed to fetch iterations: {response.text}")
        data = response.json()
        target = iteration_name.strip().lower().replace('/', '\\')
        for it in data.get("value", []):
            it_name = it.get("name", "").strip().lower().replace('/', '\\')
            it_path = it.get("path", "").strip().lower().replace('/', '\\')
            if it_name == target or it_path == target or it_path.endswith('\\' + target):
                return it
        raise Exception(f"Iteration '{iteration_name}' not found.")

    def preview_sync(self, target_iteration_name=None):
        try:
            if target_iteration_name:
                iteration = self.get_iteration_by_name(target_iteration_name)
            else:
                iteration = self.get_current_iteration()
            iteration_name = iteration["name"]
            iteration_path = iteration["path"]
            
            work_items = self.get_iteration_work_items(iteration_path)
            
            us_assigned = 0
            us_completed = 0
            sp_assigned = 0.0
            sp_completed = 0.0
            user_stories = []

            for wi in work_items:
                fields = wi.get("fields", {})
                wi_id = wi.get("id")
                title = fields.get("System.Title", "(No Title)")
                state = fields.get("System.State", "")
                points = float(fields.get("Microsoft.VSTS.Scheduling.StoryPoints") or 0)
                work_item_type = fields.get("System.WorkItemType", "")
                
                us_assigned += 1
                sp_assigned += points
                
                is_completed = state in ["Closed", "Done", "Resolved"]
                if is_completed:
                    us_completed += 1
                    sp_completed += points

                user_stories.append({
                    "id": wi_id,
                    "title": title,
                    "state": state,
                    "story_points": points,
                    "type": work_item_type,
                    "completed": is_completed
                })

            return {
                "iteration_name": iteration_name,
                "usAssigned": us_assigned,
                "usCompleted": us_completed,
                "spAssigned": sp_assigned,
                "spCompleted": sp_completed,
                "user_stories": user_stories
            }
        except Exception as e:
            raise Exception(f"ADO Sync Error: {str(e)}")
