import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import urllib.parse

class ADOClient:
    def __init__(self, org, project, pat, team):
        self.org = org.strip() if org else ""
        self.project = project.strip() if project else ""
        self.pat = pat.strip() if pat else ""
        self.team = team.strip() if team else ""
        self.encoded_org = urllib.parse.quote(self.org)
        self.encoded_project = urllib.parse.quote(self.project)
        self.encoded_team = urllib.parse.quote(self.team)
        self.base_url = f"https://dev.azure.com/{self.encoded_org}/{self.encoded_project}"

    def get_team_area_paths(self):
        """
        Fetches the Area Path(s) configured for this team in Azure DevOps.
        If the user entered a full Area Path directly in the team field (contains '\\'), returns it.
        Otherwise queries the ADO teamfieldvalues REST API.
        """
        # If user explicitly entered a full Area Path with slashes
        if "\\" in self.team:
            return [self.team]

        url = f"{self.base_url}/{self.encoded_team}/_apis/work/teamsettings/teamfieldvalues?api-version=6.0"
        try:
            response = requests.get(url, auth=HTTPBasicAuth("", self.pat), timeout=15)
            if response.status_code == 200:
                data = response.json()
                paths = []
                for v in data.get("values", []):
                    val = v.get("value")
                    if val and val not in paths:
                        paths.append(val)
                default_val = data.get("defaultValue")
                if default_val and default_val not in paths:
                    paths.insert(0, default_val)
                if paths:
                    return paths
        except Exception as e:
            print(f"[!] Warning: Failed to query teamfieldvalues: {e}")

        # Fallback: if project and team exist, synthesize '{project}\\{team}'
        if self.team:
            return [f"{self.project}\\{self.team}"]
        return []

    def get_current_iteration(self):
        url = f"{self.base_url}/{self.encoded_team}/_apis/work/teamsettings/iterations?api-version=6.0&$timeframe=current"
        response = requests.get(url, auth=HTTPBasicAuth("", self.pat), timeout=15)
        if response.status_code == 401:
            raise Exception(f"401 Unauthorized - The configured PAT does not have access to organization '{self.org}'. Please ensure the PAT was created for organization '{self.org}' with 'Work Items (Read)' scope.")
        elif response.status_code != 200:
            err_msg = response.text.strip() or response.reason or f"HTTP {response.status_code}"
            raise Exception(f"Failed to fetch current iteration ({response.status_code}): {err_msg}")
        data = response.json()
        if data.get("count", 0) == 0:
            raise Exception("No active iteration found.")
        return data["value"][0]

    def get_iteration_work_items(self, iteration_path, area_paths=None):
        safe_project = self.project.replace("'", "''")
        safe_path = iteration_path.replace("'", "''")
        
        # Build Area Path condition
        area_filter = ""
        if area_paths:
            clauses = []
            for p in area_paths:
                if p:
                    safe_p = p.replace("'", "''")
                    clauses.append(f"[System.AreaPath] UNDER '{safe_p}'")
            if len(clauses) == 1:
                area_filter = f"AND {clauses[0]}"
            elif len(clauses) > 1:
                area_filter = f"AND ({' OR '.join(clauses)})"

        url = f"https://dev.azure.com/{self.encoded_org}/{self.encoded_project}/_apis/wit/wiql?api-version=6.0"
        
        query = f"""
        SELECT [System.Id], [System.Title], [System.State], [Microsoft.VSTS.Scheduling.StoryPoints]
        FROM workitems
        WHERE [System.TeamProject] = '{safe_project}'
        AND [System.IterationPath] = '{safe_path}'
        {area_filter}
        AND [System.WorkItemType] IN ('User Story', 'Task')
        """
        response = requests.post(url, auth=HTTPBasicAuth("", self.pat), json={"query": query}, timeout=20)
        if response.status_code == 401:
            raise Exception(f"401 Unauthorized - The configured PAT does not have access to organization '{self.org}'. Please verify PAT permissions.")
        elif response.status_code != 200:
            err_msg = response.text.strip() or response.reason or f"HTTP {response.status_code}"
            raise Exception(f"Failed to execute WIQL ({response.status_code}): {err_msg}")
        
        data = response.json()
        work_item_relations = data.get("workItems", [])
        if not work_item_relations:
            return []

        # Get details for these work items (including Title) in chunks of 200
        ids = [str(item["id"]) for item in work_item_relations]
        fields = "System.Id,System.Title,System.State,System.WorkItemType,Microsoft.VSTS.Scheduling.StoryPoints,System.AssignedTo"
        
        all_details = []
        chunk_size = 200
        for i in range(0, len(ids), chunk_size):
            chunk_ids = ids[i:i+chunk_size]
            ids_str = ",".join(chunk_ids)
            details_url = (
                f"https://dev.azure.com/{self.encoded_org}/{self.encoded_project}/_apis/wit/workitems"
                f"?ids={ids_str}&fields={fields}&api-version=6.0"
            )
            details_res = requests.get(details_url, auth=HTTPBasicAuth("", self.pat), timeout=20)
            if details_res.status_code == 401:
                raise Exception(f"401 Unauthorized while fetching work item details for org '{self.org}'.")
            elif details_res.status_code != 200:
                err_msg = details_res.text.strip() or details_res.reason or f"HTTP {details_res.status_code}"
                raise Exception(f"Failed to fetch work item details ({details_res.status_code}): {err_msg}")
            all_details.extend(details_res.json().get("value", []))
            
        return all_details

    def get_iteration_by_name(self, iteration_name: str):
        url = f"{self.base_url}/{self.encoded_team}/_apis/work/teamsettings/iterations?api-version=6.0"
        response = requests.get(url, auth=HTTPBasicAuth("", self.pat), timeout=15)
        if response.status_code == 401:
            raise Exception(f"401 Unauthorized - The configured PAT does not have access to organization '{self.org}'. Please ensure the PAT was created for organization '{self.org}' with 'Work Items (Read)' scope.")
        elif response.status_code != 200:
            err_msg = response.text.strip() or response.reason or f"HTTP {response.status_code}"
            raise Exception(f"Failed to fetch iterations ({response.status_code}): {err_msg}")
        data = response.json()
        target = iteration_name.strip().lower().replace('/', '\\')
        for it in data.get("value", []):
            it_name = it.get("name", "").strip().lower().replace('/', '\\')
            it_path = it.get("path", "").strip().lower().replace('/', '\\')
            if it_name == target or it_path == target or it_path.endswith('\\' + target) or target.endswith('\\' + it_name):
                return it
        
        # If not found directly in team settings iterations list, but input looks like a full path (contains '\\'),
        # synthesize an iteration object so WIQL can query the iteration path directly!
        if '\\' in iteration_name:
            simple_name = iteration_name.split('\\')[-1].strip()
            return {"name": simple_name, "path": iteration_name.strip()}

        raise Exception(f"Iteration '{iteration_name}' not found under team '{self.team}'.")

    def preview_sync(self, target_iteration_name=None):
        try:
            if target_iteration_name:
                iteration = self.get_iteration_by_name(target_iteration_name)
            else:
                iteration = self.get_current_iteration()
            iteration_name = iteration["name"]
            iteration_path = iteration["path"]
            
            # Retrieve team area path(s) to scope work items strictly to this team
            area_paths = self.get_team_area_paths()
            work_items = self.get_iteration_work_items(iteration_path, area_paths=area_paths)
            
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
                
                assignee_raw = fields.get("System.AssignedTo")
                assignee = (
                    assignee_raw.get("displayName")
                    if isinstance(assignee_raw, dict)
                    else (str(assignee_raw) if assignee_raw else "Unassigned")
                )
                
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
                    "assignee": assignee,
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
