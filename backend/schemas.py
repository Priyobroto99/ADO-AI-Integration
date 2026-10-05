from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "editor"
    team_id: Optional[int] = None
    new_team_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    team_id: Optional[int] = None

    class Config:
        from_attributes = True

class SprintBase(BaseModel):
    name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class SprintCreate(SprintBase):
    pass

class SprintResponse(SprintBase):
    id: int
    class Config:
        from_attributes = True

class TeamBase(BaseModel):
    engagement: str
    spoc: str

class TeamResponse(TeamBase):
    id: int
    ado_org: Optional[str] = None
    ado_project: Optional[str] = None
    ado_team: Optional[str] = None
    ado_iteration: Optional[str] = None
    # We do NOT return the PAT in the response for security reasons

    class Config:
        from_attributes = True

class ADOConfigUpdate(BaseModel):
    ado_org: Optional[str] = None
    ado_project: Optional[str] = None
    ado_team: Optional[str] = None
    ado_pat: Optional[str] = None
    ado_iteration: Optional[str] = None
    class Config:
        from_attributes = True

class TeamConfigBase(BaseModel):
    spAssigned_expected: Optional[float] = 8.0
    spAssigned_variance: Optional[float] = 3.0
    spCompleted_expected: Optional[float] = 8.0
    spCompleted_variance: Optional[float] = 3.0
    usPushed_expected: Optional[float] = 0.0
    usPushed_variance: Optional[float] = 1.0
    defectLeakage_expected: Optional[float] = 5.0
    defectLeakage_variance: Optional[float] = 5.0
    prodIncidents_expected: Optional[float] = 0.0
    prodIncidents_variance: Optional[float] = 2.0
    openRisks_expected: Optional[float] = 2.0
    openRisks_variance: Optional[float] = 2.0
    escalations_expected: Optional[float] = 0.0
    escalations_variance: Optional[float] = 2.0
    autoCoverage_expected: Optional[float] = 75.0
    autoCoverage_variance: Optional[float] = 20.0
    autoStability_expected: Optional[float] = 95.0
    autoStability_variance: Optional[float] = 10.0
    autoToolsReq_expected: Optional[float] = 0.0
    autoToolsReq_variance: Optional[float] = 1.0
    buildToolsReq_expected: Optional[float] = 0.0
    buildToolsReq_variance: Optional[float] = 1.0

class TeamConfigCreate(TeamConfigBase):
    pass

class TeamConfigResponse(TeamConfigBase):
    id: int
    team_id: int
    class Config:
        from_attributes = True

class MetricBase(BaseModel):
    engagement: Optional[str] = None
    spoc: Optional[str] = None
    sprint_id: Optional[int] = None
    sprint: Optional[str] = None
    spAssigned: Optional[float] = None
    spCompleted: Optional[float] = None
    usAssigned: Optional[float] = None
    usCompleted: Optional[float] = None
    usPushed: Optional[float] = None
    defectLeakage: Optional[float] = None
    prodIncidents: Optional[float] = None
    openRisks: Optional[float] = None
    sowMilestones: Optional[str] = None
    escalations: Optional[float] = None
    autoToolsReq: Optional[str] = None
    buildToolsReq: Optional[str] = None
    autoCoverage: Optional[float] = None
    autoStability: Optional[float] = None
    regRunTime: Optional[float] = None
    regExecTimeNoAuto: Optional[float] = None
    autoBugs: Optional[float] = None
    kt: Optional[float] = None
    assets: Optional[float] = None

class MetricResponse(MetricBase):
    id: int
    team_id: int
    class Config:
        from_attributes = True

class DetailBase(BaseModel):
    engagement: Optional[str] = None
    spoc: Optional[str] = None
    sprint_id: Optional[int] = None
    sprint: Optional[str] = None
    usAssignedPts: Optional[str] = None
    defectPts: Optional[str] = None
    incidentPts: Optional[str] = None
    riskPts: Optional[str] = None
    sowPts: Optional[str] = None
    escalationPts: Optional[str] = None
    autoToolPts: Optional[str] = None
    buildToolPts: Optional[str] = None
    cloudProf: Optional[str] = None
    cicdSetup: Optional[str] = None
    ktPrep: Optional[str] = None
    autoBugsPts: Optional[str] = None
    cicdMat: Optional[str] = None
    assetPts: Optional[str] = None
    deloitteTime: Optional[str] = None
    tenroxTime: Optional[str] = None
    catManager: Optional[str] = None
    engagementCode: Optional[str] = None
    lobLead: Optional[str] = None
    processComp: Optional[float] = None

class DetailResponse(DetailBase):
    id: int
    team_id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
