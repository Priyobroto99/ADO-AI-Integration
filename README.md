# CAT Delivery Excellence Tracker

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Version](https://img.shields.io/badge/Version-1.1.0-blue)
![Stack](https://img.shields.io/badge/Stack-FastAPI%20|%20PostgreSQL%20|%20TailwindCSS%20|%20Tremor-orange)

The **CAT Delivery Excellence Tracker** is a comprehensive, centralized dashboard for tracking, aggregating, and assessing the delivery metrics, program health, capability, automation, and compliance of multiple agile teams. 

It seamlessly integrates with **Azure DevOps (ADO)** to automatically pull sprint data (Story Points, User Stories, Tasks), supports selective ingestion by team member (QA filter), provides interactive overwrite protection, and uses dynamically configurable **RAG (Red/Amber/Green)** thresholds to automatically generate Early Warning Indicators for leadership and stakeholders.

> [!TIP]
> * For an executive breakdown, value proposition, and detailed feature matrix, see the [Product Overview & Pitch Guide](docs/PRODUCT_OVERVIEW.md).
> * For the security architecture, permissions matrix, and role enforcement guide, see [Roles & Access Guide](docs/ROLES_AND_ACCESS.md).
> * For database schema, data dictionary, and disaster recovery rebuild instructions, see [Database Structure & Rebuild Guide](docs/DATABASE_STRUCTURE.md).
> * For architectural details on static vs. rolling sprint data separation, see [Sprint Data Separation Architecture](docs/SPRINT_DATA_SEPARATION.md) and [Sprint Data Change Table](docs/SPRINT_DATA_CHANGE_TABLE.md).

---

## 🌟 Key Features

*   📊 **Unified Dashboard view:** Consolidated RAG statuses across all active projects for a chosen Sprint with portfolio-level Early Warning Indicators.
*   🔄 **Selective Azure DevOps Integration:** 
    *   One-click live syncing of User Stories, Tasks, and Story Points via ADO Personal Access Tokens (PAT).
    *   **QA Team Member Filtering:** Interactive dialog allowing SPOCs to select/deselect specific team members so only QA work items are ingested.
    *   **Sprint Overwrite Safeguards:** Detects existing sprint data and requires explicit confirmation before updating the database.
*   🏷️ **User Story vs. Task Distinction:**
    *   Visual color-coded badges for **User Stories** (blue) and **Tasks** (amber) across all views.
    *   Detailed breakdown metrics (Total Items, Stories Count, Tasks Count, Story Points).
    *   Dynamic table search and filtering by work item type.
*   ⏱️ **Static vs. Rolling Sprint Data Architecture:**
    *   **Rolling Sprint Data:** Sprint delivery metrics, story points, and timesheet compliance captured per sprint iteration.
    *   **Static Team Profiles:** Persistent team capabilities, automation tooling, and program health (Prod Incidents, SOW Milestones, Escalations, Open Risks) configured once and updated on demand without redundant re-entry.
*   ⚙️ **Customizable RAG Thresholds:** Admin controls to set exact baseline thresholds for Green/Amber/Red ratings per team for metrics like Defect Leakage, Automation Coverage, etc.
*   📋 **Comprehensive KPI Tracking:** 
    *   **Delivery:** Velocity, Spill-overs, User Stories and Tasks breakdown.
    *   **Health:** Defect Leakage, Prod Incidents, Open Risks, SOW Milestones, Escalations.
    *   **Capability & Automation:** CI/CD Maturity, Cloud Proficiency, Automation Stability, Tooling Competency.
    *   **Compliance:** Deloitte & Tenrox Timesheet completions.

---

## 🏗️ System Architecture & Workflows

### High-Level Architecture

```mermaid
graph TD
    A[Frontend Client - HTML/JS/Tailwind] <-->|REST API| B(FastAPI Backend)
    B <-->|SQLAlchemy ORM| C[(PostgreSQL Database)]
    B <-->|ADO REST API| D[Azure DevOps]
    
    subgraph UI Layers
    A1[Main Dashboard]
    A2[Team Drill-Down: Delivery, Health, Automation, Compliance]
    A3[Data Entry / Update Portal]
    A --> A1
    A --> A2
    A --> A3
    end

    subgraph Data Domains
    C --> C1[(Rolling Sprint Metrics)]
    C --> C2[(Static Team Profiles)]
    C --> C3[(RAG Threshold Configs)]
    end
```

### Data Synchronization Flow (Selective ADO Sync)

The tool saves SPOCs (Single Points of Contact) time by automatically extracting sprint data from ADO, providing interactive team-member filters, and non-destructively merging with qualitative metrics:

```mermaid
sequenceDiagram
    participant SPOC
    participant UI as Tracker UI
    participant API as FastAPI Backend
    participant ADO as Azure DevOps
    participant DB as Database

    SPOC->>UI: Selects Team & Sprint, clicks "Sync ADO Data"
    UI->>API: GET /teams/{team_id}/ado-preview?sprint={sprint}
    API->>ADO: Query WIQL for User Stories & Tasks via PAT
    ADO-->>API: Returns Assigned Work Items & Story Points
    API-->>UI: Returns work items & assignee metadata
    UI->>UI: Checks if sprint has existing data (triggers overwrite warning if found)
    UI-->>SPOC: Displays Review Modal with QA Team Member Checkboxes
    SPOC->>UI: Toggles team members (Select All / Deselect QA members)
    UI->>UI: Dynamically recalculates Stories, Tasks, & Story Points
    SPOC->>UI: Confirms overwrite checkbox & clicks "Update Database"
    UI->>API: PUT /metrics & PUT /details (Filtered Stories & Points)
    API->>DB: Persists merged data for the selected sprint
    UI->>SPOC: Displays success confirmation and refreshes dashboard
```

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   PostgreSQL Database (Neon / local)
*   Docker & Docker Compose (optional for containerized deployment)
*   Node.js (for frontend syntax testing if developing)

### Installation & Local Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Priyobroto99/ADO-AI-Integration.git
   cd ADO-AI-Integration
   ```

2. **Set up the Database environment:**
   Create a `.env` file in the `backend/` directory:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=require
   SECRET_KEY=your_secure_jwt_secret_key
   ```

3. **Install dependencies and run the server:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

4. **Launch the Frontend:**
   Open `frontend/cat_dashboard.html` in your browser, or serve it using a local HTTP server:
   ```bash
   python -m http.server 8080 --directory frontend
   ```

### Running with Docker Compose

To run both backend and frontend in containerized mode:
```bash
docker compose up -d --build
```
*   **Frontend Dashboard:** `http://localhost:8080` (or `http://localhost:80`)
*   **FastAPI Backend & Swagger Docs:** `http://localhost:8000/docs`

---

## 📖 User Guide

### 1. Onboarding a New Team & Static Profile
Before metrics can be tracked, the team must be added to the system:
*   Login with an `admin` account.
*   Navigate to the **Update Team Data** tab.
*   Configure the team's `ADO Organization`, `Project Name`, `Team Name (Area)`, and provide a secure `Personal Access Token` for sync capabilities.
*   Set up the team's **Static Profile** (CAT Manager, LOB Lead, CI/CD Maturity, Automation Tooling, SOW Milestones). These static attributes persist across all sprints automatically.

### 2. Creating and Managing Sprints
Sprints are managed globally across all teams to ensure standardized reporting:
*   In the **Update Team Data** view, click the **`+`** icon next to the Sprint dropdown.
*   Enter the Sprint Name (e.g. "Sprint 7") and the Start/End dates.
*   The sprint will instantly become available for data entry across all teams.

### 3. Updating Team Metrics & ADO Sync

1. Select your Team and the target Sprint in the **Update Team Data** tab.
2. Click **Sync ADO Data**. The tool queries Azure DevOps for the matching Iteration Path.
3. **QA Team Member Selection:**
   * In the review dialog, inspect the list of assignees.
   * Uncheck any non-QA team members. Metrics (Stories count, Tasks count, Story Points) update in real-time.
4. **Existing Data Overwrite Protection:**
   * If the sprint already contains recorded data, a prominent alert warning will appear.
   * Check the confirmation box: *"I understand and confirm overwriting this sprint's existing data with selected ADO items"*.
5. Click **Confirm & Update DB**. This writes the selected work items and story points to the database while preserving all qualitative notes.

> [!NOTE]
> **Work Item Filtering Scope (User Stories & Tasks):**
> The ADO synchronization query filters for `[System.WorkItemType] IN ('User Story', 'Task')` to measure feature delivery and velocity accurately. While the ADO integration client is capable of fetching bugs, **Bugs** are intentionally excluded from sprint delivery work items to prevent skewing velocity counts.

### 4. US Assigned Details Editor & Pipe Support
* The **US Assigned Details** editor in the Update tab allows manual editing or addition of work items.
* **Multiline & Pipe Separation:**
  * Enter one item per line, or separate with `||`.
  * Story titles with internal pipe characters (`|`) are safely preserved and not broken into spurious extra items.
* **Work Item Type Prefix:** You can explicitly tag items using `[Task]` or `[User Story]` prefixes (e.g. `[#12345] [Task] Automation test suite`).
* Use the **Lines View** and **Pipes View** formatting buttons for instant restructuring.
* Expand the **Parsed Work Items Breakdown** drawer to preview individual item badges, story points, and assignees.

### 5. Delivery Tab: User Stories & Tasks Assigned Table
* Displays a dedicated **Type** column distinguishing **User Story** (blue badge) from **Task** (amber badge).
* Summary badges display the exact count: `Total Items`, `X Stories`, `Y Tasks`, `Story Points`, `Completed`, and `Assigned`.
* Filter input allows quick real-time searching by title, assignee, or work item type (`task`, `story`).

---

## 🛠️ Tech Stack & Concepts

*   **Backend:** FastAPI provides robust, asynchronous REST endpoints with Pydantic schema validation. SQLAlchemy manages ORM mapping to PostgreSQL.
*   **Frontend UI:** Vanilla JavaScript drives the state management (`globalData`), injecting data into a responsive Tailwind CSS grid populated with Tremor UI components for a clean, modern aesthetic.
*   **Security:** Passwords and ADO PATs are securely hashed and managed. JWT tokens handle user sessions with role-based access control (`admin`, `editor`, `team_spoc`).

---
*Created and maintained by the CAT Delivery Excellence team.*
