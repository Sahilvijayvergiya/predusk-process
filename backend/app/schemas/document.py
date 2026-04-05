from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Import JobStatus from models to avoid duplication
from app.models.document import JobStatus


class DocumentCreate(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    file_type: str
    file_size: int


class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_type: str
    file_size: int
    upload_time: datetime

    class Config:
        from_attributes = True


class ProcessingJobCreate(BaseModel):
    document_id: int


class ProcessingJobUpdate(BaseModel):
    status: Optional[JobStatus] = None
    progress_percentage: Optional[float] = None
    current_stage: Optional[str] = None
    error_message: Optional[str] = None
    extracted_title: Optional[str] = None
    extracted_category: Optional[str] = None
    extracted_summary: Optional[str] = None
    extracted_keywords: Optional[List[str]] = None
    processed_content: Optional[str] = None
    final_result: Optional[Dict[str, Any]] = None
    is_reviewed: Optional[bool] = None
    is_finalized: Optional[bool] = None


class ProcessingJobResponse(BaseModel):
    id: int
    document_id: int
    status: JobStatus
    progress_percentage: float
    current_stage: str
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    extracted_title: Optional[str] = None
    extracted_category: Optional[str] = None
    extracted_summary: Optional[str] = None
    extracted_keywords: Optional[List[str]] = None
    processed_content: Optional[str] = None
    final_result: Optional[Dict[str, Any]] = None
    is_reviewed: bool
    is_finalized: bool
    celery_task_id: Optional[str] = None

    class Config:
        from_attributes = True


class ProgressEvent(BaseModel):
    job_id: int
    status: JobStatus
    progress_percentage: float
    current_stage: str
    message: Optional[str] = None
    timestamp: datetime
