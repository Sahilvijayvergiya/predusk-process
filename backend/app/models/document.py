from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class JobStatus(enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with processing jobs
    processing_jobs = relationship("ProcessingJob", back_populates="document")


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.QUEUED, nullable=False)
    progress_percentage = Column(Float, default=0.0)
    current_stage = Column(String, default="queued")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Processing results
    extracted_title = Column(Text, nullable=True)
    extracted_category = Column(String, nullable=True)
    extracted_summary = Column(Text, nullable=True)
    extracted_keywords = Column(JSON, nullable=True)
    processed_content = Column(Text, nullable=True)
    final_result = Column(JSON, nullable=True)
    
    # Review and finalization
    is_reviewed = Column(String, default=False)
    is_finalized = Column(String, default=False)
    
    # Relationship with document
    document = relationship("Document", back_populates="processing_jobs")
    
    # Celery task ID
    celery_task_id = Column(String, nullable=True)
