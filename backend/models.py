from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="editor")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    engagement = Column(String, unique=True, index=True)
    spoc = Column(String)

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
