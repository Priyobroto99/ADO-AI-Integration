# CAT Delivery Excellence Tracker

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Stack](https://img.shields.io/badge/Stack-FastAPI%20|%20PostgreSQL%20|%20TailwindCSS%20|%20Tremor-orange)

The **CAT Delivery Excellence Tracker** is a comprehensive, centralized dashboard for tracking, aggregating, and assessing the delivery metrics, program health, capability, automation, and compliance of multiple agile teams. 

It seamlessly integrates with **Azure DevOps (ADO)** to automatically pull sprint data (Story Points, User Stories) and uses dynamically configurable **RAG (Red/Amber/Green)** thresholds to automatically generate Early Warning Indicators for leadership and stakeholders.

---

## 🌟 Key Features

*   📊 **Unified Dashboard view:** Consolidated RAG statuses across all active projects for a chosen Sprint.
*   🔄 **Azure DevOps Integration:** One-click syncing of User Stories and Story Points via ADO Personal Access Tokens (PAT).
*   ⏱️ **Sprint-Level Granularity:** Deep dive into specific iterations with precise history tracking. Manually create new sprints on the fly.
*   ⚙️ **Customizable RAG Thresholds:** Admin controls to set exact baseline thresholds for Green/Amber/Red ratings per team for metrics like Defect Leakage, Automation Coverage, etc.
*   📋 **Comprehensive KPI Tracking:** 
    *   **Delivery:** Velocity, Spill-overs.
    *   **Health:** Defect Leakage, Prod Incidents, Open Risks, Escalations.
    *   **Capability & Automation:** CI/CD Maturity, Cloud Proficiency, Automation Stability.
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
    A2[Team Drill-Down]
    A3[Data Entry / Config]
    A --> A1
    A --> A2
    A --> A3
    end
```

### Data Synchronization Flow (ADO Sync)

The tool saves SPOCs (Single Points of Contact) time by automatically extracting sprint data from ADO and merging it non-destructively with manually entered qualitative metrics.

```mermaid
sequenceDiagram
    participant SPOC
    participant UI as Tracker UI
    participant API as FastAPI Backend
    participant ADO as Azure DevOps
    participant DB as Database

    SPOC->>UI: Selects Team & Sprint, clicks "Sync ADO Data"
    UI->>API: GET /teams/{team_id}/ado-preview?sprint={sprint}
    API->>ADO: Fetch Iteration details via PAT
    ADO-->>API: Returns Assigned/Completed SPs & User Stories
    API-->>UI: Displays Preview Modal to SPOC
    SPOC->>UI: Reviews and clicks "Confirm & Update DB"
    UI->>UI: Merges ADO data with existing manual metrics (e.g. Risks)
    UI->>API: PUT /metrics & PUT /details
    API->>DB: Persists merged data for the selected sprint
    UI->>SPOC: Displays success and updates dashboard
```

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   PostgreSQL Database
*   Node.js (for frontend syntax testing if developing)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Priyobroto99/ADO-AI-Integration.git
   cd ADO-AI-Integration
   ```

2. **Set up the Database environment:**
   Create a `.env` file in the `backend/` directory:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/dbname
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

---

## 📖 User Guide

### 1. Onboarding a New Team
Before metrics can be tracked, the team must be added to the system.
*   Login with an `admin` account.
*   Navigate to the **Update Team Data** tab.
*   Configure the team's `ADO Organization`, `Project Name`, `Team Name (Area)`, and provide a secure `Personal Access Token` for sync capabilities.

### 2. Creating and Managing Sprints
Sprints are managed globally across all teams to ensure standard reporting.
*   In the **Update Team Data** view, click the **`+`** icon next to the Sprint dropdown.
*   Enter the Sprint Name (e.g. "Sprint 7") and the Start/End dates.
*   The sprint will instantly become available for data entry across all teams.

### 3. Updating Team Metrics & ADO Sync
*   Select your Team and the current Sprint in the update view.
*   Click **Sync ADO Data**. The tool will fetch exactly what is in ADO for the matching Iteration Path.
*   Review the pulled Story Points and User Story titles in the pop-up modal.
*   Click **Confirm & Update DB**. This will safely *merge* the ADO data with any manual fields (like Defect Leakages or Timesheet compliance) without overwriting them.

### 4. Viewing the Dashboard
```mermaid
flowchart LR
    A[Global Sprint Dropdown] -->|Filters| B(Main Dashboard)
    A -->|Filters| C(Delivery Tab)
    A -->|Filters| D(Program Health Tab)
    
    B --> E[All Projects Overview Table]
    B --> F[Aggregated Early Warnings]
```
*   Use the **Top-Left Sprint Dropdown** to globally filter the entire application.
*   The **Main Dashboard** provides a bird's eye view of all projects for the selected sprint.
*   Switch to tabs like **Delivery** or **Program Health** to drill into the specific metrics for a single team.

---

## 🛠️ Tech Stack & Concepts

*   **Backend:** FastAPI provides robust, asynchronous REST endpoints with Pydantic schema validation. SQLAlchemy manages ORM mapping to PostgreSQL.
*   **Frontend UI:** Vanilla JavaScript drives the state management (`globalData`), injecting data into a responsive Tailwind CSS grid populated with Tremor UI components for a clean, modern aesthetic.
*   **Security:** Passwords and ADO PATs are securely hashed and managed. JWT tokens handle user sessions.

---
*Created and maintained by the CAT Delivery Excellence team.*
