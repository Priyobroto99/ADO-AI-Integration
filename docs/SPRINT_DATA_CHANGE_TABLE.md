# Static & Sprint Data Separation — Comprehensive Change Table

This document details the exact **As-Is (Current State)** vs. **To-Be (Proposed State)** changes across the Database Schema, Data Fields, Backend APIs, and Frontend User Interface.

---

## 1. Database Schema & Architecture Changes

| Component | Current State (As-Is) | Proposed State (To-Be) | Change Type | Justification / Impact |
| :--- | :--- | :--- | :--- | :--- |
| **`teams` table** | Stores `id, engagement, spoc, ado_*` configuration. | Unchanged. Holds core team identity & ADO credentials. | No Change | Core anchor table for all team-related data. |
| **`sprints` table** | Stores `id, name, start_date, end_date`. | Unchanged. Holds iteration timelines. | No Change | Anchor table for sprint periods. |
| **`team_configs` table** | Stores RAG expected/variance thresholds per team. | Unchanged. 1-to-1 with `teams`. | No Change | Preserves custom team thresholds. |
| **`team_profiles` table** *(NEW)* | Did not exist. Static fields were repeated in `metrics` and `details` for every sprint. | **New Table (1-to-1 with `teams`)**: Holds all persistent, team-level capabilities, automation suite metrics, general management info, and rolling risks. | **New Entity** | Eliminates static data duplication; ensures team capabilities never go blank when switching sprints. |
| **`metrics` table** | Contained 23 columns mixing sprint metrics (`spAssigned`, `usAssigned`) with static metrics (`autoCoverage`, `autoStability`, `regRunTime`). | **Transitioned to `sprint_metrics`**: Retains strictly iteration metrics (`spAssigned`, `spCompleted`, `usAssigned`, `usCompleted`, `usPushed`, `defectLeakage`, `prodIncidents`). | **Refactor** | Clearly defines iteration velocity and quality per sprint. |
| **`details` table** | Contained 24 columns mixing user story lists with static tool requirements, CI/CD setup, management names, and compliance. | **Transitioned to `sprint_details`** (or merged into `sprint_metrics`): Retains strictly iteration details (`usAssignedPts` JSON, `defectPts`, `incidentPts`, `deloitteTime`, `tenroxTime`, `processComp`). | **Refactor** | Separates the iteration work-item payload from static capability text. |

---

## 2. Field-by-Field Lifecycle & Mapping Matrix

| Field Name | Current Location | New Target Location | Classification | Source | As-Is Behavior | To-Be Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`catManager`** | `details` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Resets/blanks out if not re-entered per sprint. | Persists indefinitely per team; updated only on personnel change. |
| **`engagementCode`** | `details` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Tied to sprint record. | Fixed team-level property. |
| **`lobLead`** | `details` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Tied to sprint record. | Fixed team-level property. |
| **`cloudProf`** | `details` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Disappears on new sprint creation. | Permanent team capability indicator. |
| **`cicdSetup`** | `details` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Disappears on new sprint creation. | Permanent pipeline infrastructure indicator. |
| **`cicdMat`** | `details` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Disappears on new sprint creation. | Quarterly/rolling maturity rating. |
| **`autoToolsReq`** | `metrics` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Disappears on new sprint creation. | Tool requirements remain open until marked resolved. |
| **`autoToolPts`** | `details` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Disappears on new sprint creation. | Tool list persists across all sprint views. |
| **`buildToolsReq`** | `metrics` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Disappears on new sprint creation. | Build tool requirements remain open until resolved. |
| **`buildToolPts`** | `details` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Disappears on new sprint creation. | Tool list persists across all sprint views. |
| **`autoCoverage`** | `metrics` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Blanks out unless copied. | Reflects overall repo automation coverage %. |
| **`autoStability`** | `metrics` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Blanks out unless copied. | Reflects ongoing test suite health. |
| **`regRunTime`** | `metrics` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Blanks out unless copied. | Automated run duration baseline. |
| **`regExecTimeNoAuto`** | `metrics` (per sprint) | `team_profiles` | **Static** | SPOC Manual | Blanks out unless copied. | Manual test cycle baseline. |
| **`kt` / `ktPrep`** | `metrics`/`details` | `team_profiles` | **Static** | SPOC Manual | Blanks out unless copied. | Ongoing knowledge transfer status. |
| **`assets` / `assetPts`** | `metrics`/`details` | `team_profiles` | **Static** | SPOC Manual | Blanks out unless copied. | Cumulative reusable asset catalog. |
| **`autoBugs` / `autoBugsPts`** | `metrics`/`details` | `team_profiles` | **Static** | SPOC Manual | Blanks out unless copied. | Active framework bug count. |
| **`openRisks` / `riskPts`** | `metrics`/`details` | `team_profiles` | **Static (Rolling)** | SPOC Manual | Disappears if not cloned each sprint. | Ongoing program risk register (persists until closed). |
| **`sowMilestones` / `sowPts`** | `metrics`/`details` | `team_profiles` | **Static (Rolling)** | SPOC Manual | Disappears if not cloned each sprint. | Contractual milestones and target dates. |
| **`escalations` / `escalationPts`** | `metrics`/`details` | `team_profiles` | **Static (Rolling)** | SPOC Manual | Disappears if not cloned each sprint. | Active RCA and operational escalations. |
| **`spAssigned`** | `metrics` (per sprint) | `sprint_metrics` | **Sprint** | **ADO Sync** | Scoped to sprint. | Unchanged: strictly iteration committed points. |
| **`spCompleted`** | `metrics` (per sprint) | `sprint_metrics` | **Sprint** | **ADO Sync** | Scoped to sprint. | Unchanged: strictly iteration completed points. |
| **`usAssigned`** | `metrics` (per sprint) | `sprint_metrics` | **Sprint** | **ADO Sync** | Scoped to sprint. | Unchanged: strictly iteration committed stories count. |
| **`usCompleted`** | `metrics` (per sprint) | `sprint_metrics` | **Sprint** | **ADO Sync** | Scoped to sprint. | Unchanged: strictly iteration completed stories count. |
| **`usPushed`** | `metrics` (per sprint) | `sprint_metrics` | **Sprint** | SPOC / ADO | Scoped to sprint. | Unchanged: stories pushed to next iteration. |
| **`usAssignedPts`** | `details` (per sprint) | `sprint_metrics` | **Sprint** | **ADO Sync** | Previously joined by pipe or newline. | **Structured JSON array**: `[{ id, title, story_points, assignee, state, type }]`. |
| **`defectLeakage`** | `metrics` (per sprint) | `sprint_metrics` | **Sprint** | SPOC / ADO | Scoped to sprint. | Defects found in production/QA during this sprint. |
| **`prodIncidents`** | `metrics` (per sprint) | `sprint_metrics` | **Sprint** | SPOC / ADO | Scoped to sprint. | Incidents occurring during this sprint. |
| **`defectPts`** | `details` (per sprint) | `sprint_metrics` | **Sprint** | SPOC / ADO | Scoped to sprint. | Defect descriptions for this sprint. |
| **`incidentPts`** | `details` (per sprint) | `sprint_metrics` | **Sprint** | SPOC / ADO | Scoped to sprint. | Incident descriptions for this sprint. |
| **`deloitteTime`** | `details` (per sprint) | `sprint_metrics` | **Sprint** | SPOC Manual | Scoped to sprint. | Timesheet compliance for this sprint cycle. |
| **`tenroxTime`** | `details` (per sprint) | `sprint_metrics` | **Sprint** | SPOC Manual | Scoped to sprint. | Tenrox compliance for this sprint cycle. |
| **`processComp`** | `details` (per sprint) | `sprint_metrics` | **Sprint** | Calculated | Scoped to sprint. | Computed % compliance for this sprint cycle. |

---

## 3. Backend API Changes

| Endpoint | Method | Current Behavior (As-Is) | Proposed Behavior (To-Be) | Change Type |
| :--- | :--- | :--- | :--- | :--- |
| **`/teams/{id}/profile`** | `GET` | Did not exist. Client had to inspect `metrics` and `details` for random records. | Returns the team's active static profile (`catManager`, `cloudProf`, automation metrics, risks). | **New Endpoint** |
| **`/teams/{id}/profile`** | `PUT` | Did not exist. SPOC had to select a sprint to update static fields. | Updates the team's persistent profile once. Immediately applies across all sprint views. | **New Endpoint** |
| **`/teams/{id}/sprints/{sprint_id}`** | `GET` | Required fetching entire `metrics` and `details` arrays. | Returns strictly the delivery velocity, user stories JSON, defect leakage, and timesheet compliance for the specified sprint. | **New Endpoint** |
| **`/teams/{id}/sprints/{sprint_id}`** | `PUT` | Handled via generic `/metrics/{id}` and `/details/{id}`. | Saves iteration-specific metrics and story JSON for that sprint. | **Refactor** |
| **`/dashboard/{id}`** | `GET` | Client pulled 4 large endpoints (`/metrics`, `/details`, `/configs`, `/sprints`) and performed manual JS joins. | **Unified Composite Endpoint**: Returns `{ team, active_sprint, static_profile, sprint_metrics, rag_config }` in a single fast call. | **Enhancement** |
| **`/teams/{id}/ado-preview`** | `GET` | Fetches ADO preview with story IDs, points, assignees. | Unchanged functionality; seamlessly saves into `sprint_metrics.usAssignedPts`. | Backward Compatible |

---

## 4. Frontend User Experience Changes

| UI Area | Current State (As-Is) | Proposed State (To-Be) | User Benefit |
| :--- | :--- | :--- | :--- |
| **Sprint Dropdown (`#mainSprintSelect`)** | Selecting a new sprint resets Capability, Automation, and Health tabs to blank if data wasn't copied. | Switching sprints updates **Delivery** and **Compliance**; **Capability**, **Automation**, and **Health** remain permanently populated from the team profile. | SPOCs and leadership never see blank capability screens. |
| **Delivery Tab Details** | Used to be a basic bullet list; recently updated to interactive table with points and assignees. | Retained and expanded: displays the interactive User Stories & Tasks table scoped to the selected sprint. | Complete visibility into story points, assignees, and states. |
| **Update Team Data Modal** | 4 tabs (`metrics`, `details`, `ado`, `configs`). SPOC had to select a sprint even to edit static fields like Cat Manager or Tools Required. | **Separated into 2 Clear Domains**: <br>1. **Team Profile (Static):** Edit Capabilities, Automation, Management Info (no sprint selector). <br>2. **Sprint Delivery (Dynamic):** Select sprint, sync ADO, log sprint defects & timesheet compliance. | Reduces SPOC confusion by 80%; prevents accidental overwriting of static data. |
| **ADO Sync Modal** | Syncs stories into `details.usAssignedPts`. | Unchanged flow; saves structured JSON directly into the sprint iteration record. | Smooth, automated iteration updates. |

---

## 5. Migration & Backward Compatibility Strategy

1. **Zero Downtime Migration Script (`scripts/migrate_static_sprint_data.py`):**
   - Automatically inspects existing `metrics` and `details` tables.
   - For each team, extracts the latest non-null values for static fields (Cat Manager, Automation tools, Cloud Proficiency, etc.) and populates the new `team_profiles` table.
   - Retains all existing rows in `metrics` and `details` as historical backups.
2. **Backward-Compatible API Layer:**
   - Existing `/metrics` and `/details` GET endpoints remain functional during the transition so older clients or test scripts do not break.
   - The frontend is switched to use the clean composite profile endpoints.
