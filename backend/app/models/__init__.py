"""SQLAlchemy ORM Data Models for RubberStress."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    material_samples = relationship("MaterialSample", back_populates="owner", cascade="all, delete-orphan")
    analysis_runs = relationship("AnalysisRun", back_populates="owner", cascade="all, delete-orphan")


class MaterialSample(Base):
    __tablename__ = "material_samples"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), index=True, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="material_samples")
    analysis_runs = relationship("AnalysisRun", back_populates="material_sample")


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(String(36), primary_key=True, index=True)  # UUID string
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    material_sample_id = Column(Integer, ForeignKey("material_samples.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(50), default="queued", index=True, nullable=False)  # queued | running | done | failed
    input_file_path = Column(String(512), nullable=False)
    deformation_mode = Column(String(100), default="uniaxial", nullable=False)
    config = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    report_file_path = Column(String(512), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="analysis_runs")
    material_sample = relationship("MaterialSample", back_populates="analysis_runs")
