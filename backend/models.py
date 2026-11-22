from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="editor")
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    engagement = Column(String, unique=True, index=True)
    spoc = Column(String)
    ado_org = Column(String, nullable=True)
    ado_project = Column(String, nullable=True)
    ado_team = Column(String, nullable=True)
    ado_pat = Column(String, nullable=True)
    ado_iteration = Column(String, nullable=True)

class Sprint(Base):
    __tablename__ = "sprints"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)

class TeamConfig(Base):
    __tablename__ = "team_configs"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), unique=True)
    
    spAssigned_expected = Column(Float, default=8.0)
    spAssigned_variance = Column(Float, default=3.0)
    spCompleted_expected = Column(Float, default=8.0)
    spCompleted_variance = Column(Float, default=3.0)
    usPushed_expected = Column(Float, default=0.0)
    usPushed_variance = Column(Float, default=1.0)
    defectLeakage_expected = Column(Float, default=5.0)
    defectLeakage_variance = Column(Float, default=5.0)
    prodIncidents_expected = Column(Float, default=0.0)
    prodIncidents_variance = Column(Float, default=2.0)
    openRisks_expected = Column(Float, default=2.0)
    openRisks_variance = Column(Float, default=2.0)
    escalations_expected = Column(Float, default=0.0)
    escalations_variance = Column(Float, default=2.0)
    autoCoverage_expected = Column(Float, default=75.0)
    autoCoverage_variance = Column(Float, default=20.0)
    autoStability_expected = Column(Float, default=95.0)
    autoStability_variance = Column(Float, default=10.0)
    autoToolsReq_expected = Column(Float, default=0.0)
    autoToolsReq_variance = Column(Float, default=1.0)
    buildToolsReq_expected = Column(Float, default=0.0)
    buildToolsReq_variance = Column(Float, default=1.0)

class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    sprint_id = Column(Integer, ForeignKey("sprints.id"), nullable=True)
    sprint = Column(String, default="Sprint 1")
    spAssigned = Column(Float)
    spCompleted = Column(Float)
    usAssigned = Column(Float)
    usCompleted = Column(Float)
    usPushed = Column(Float)
    defectLeakage = Column(Float)
    prodIncidents = Column(Float)
    openRisks = Column(Float)
    sowMilestones = Column(String)
    escalations = Column(Float)
    autoToolsReq = Column(String)
    buildToolsReq = Column(String)
    autoCoverage = Column(Float)
    autoStability = Column(Float)
    regRunTime = Column(Float)
    regExecTimeNoAuto = Column(Float)
    autoBugs = Column(Float)
    kt = Column(Float)
    assets = Column(Float)

class Detail(Base):
    __tablename__ = "details"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    sprint_id = Column(Integer, ForeignKey("sprints.id"), nullable=True)
    sprint = Column(String, default="Sprint 1")
    usAssignedPts = Column(String)
    defectPts = Column(String)
    incidentPts = Column(String)
    riskPts = Column(String)
    sowPts = Column(String)
    escalationPts = Column(String)
    autoToolPts = Column(String)
    buildToolPts = Column(String)
    cloudProf = Column(String)
    cicdSetup = Column(String)
    ktPrep = Column(String)
    autoBugsPts = Column(String)
    cicdMat = Column(String)
    assetPts = Column(String)
    deloitteTime = Column(String)
    tenroxTime = Column(String)
    catManager = Column(String)
    engagementCode = Column(String)
    lobLead = Column(String)
    processComp = Column(Float)

class TeamProfile(Base):
    __tablename__ = "team_profiles"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), unique=True)
    
    # General Info
    catManager = Column(String, nullable=True)
    engagementCode = Column(String, nullable=True)
    lobLead = Column(String, nullable=True)
    
    # Capability
    cloudProf = Column(String, nullable=True)
    cicdSetup = Column(String, nullable=True)
    cicdMat = Column(String, nullable=True)
    autoToolsReq = Column(String, nullable=True)
    buildToolsReq = Column(String, nullable=True)
    autoToolPts = Column(String, nullable=True)
    buildToolPts = Column(String, nullable=True)
    
    # Automation
    autoCoverage = Column(Float, nullable=True)
    autoStability = Column(Float, nullable=True)
    regRunTime = Column(Float, nullable=True)
    regExecTimeNoAuto = Column(Float, nullable=True)
    kt = Column(Float, nullable=True)
    ktPrep = Column(String, nullable=True)
    assets = Column(Float, nullable=True)
    assetPts = Column(String, nullable=True)
    autoBugs = Column(Float, nullable=True)
    autoBugsPts = Column(String, nullable=True)
    
    # Program Health
    defectLeakage = Column(Float, nullable=True)
    prodIncidents = Column(Float, nullable=True)
    openRisks = Column(Float, nullable=True)
    sowMilestones = Column(String, nullable=True)
    escalations = Column(Float, nullable=True)
    defectPts = Column(String, nullable=True)
    incidentPts = Column(String, nullable=True)
    riskPts = Column(String, nullable=True)
    sowPts = Column(String, nullable=True)
    escalationPts = Column(String, nullable=True)
