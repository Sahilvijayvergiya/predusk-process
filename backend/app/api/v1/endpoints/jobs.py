from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import StreamingResponse
import csv
import json
from io import StringIO

from app.core.database import get_db
from app.models.document import ProcessingJob, JobStatus
from app.schemas.document import ProcessingJobResponse, ProcessingJobUpdate
from app.services.job_service import JobService

router = APIRouter()


@router.get("/", response_model=List[ProcessingJobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by filename"),
    sort_by: Optional[str] = Query("created_at", description="Sort field"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    db: Session = Depends(get_db)
):
    """List processing jobs with filtering and sorting"""
    job_service = JobService(db)
    return await job_service.list_jobs(
        skip=skip,
        limit=limit,
        status=status,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/{job_id}", response_model=ProcessingJobResponse)
async def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific processing job"""
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=ProcessingJobResponse)
async def update_job(
    job_id: int,
    job_update: ProcessingJobUpdate,
    db: Session = Depends(get_db)
):
    """Update a processing job (for review and finalization)"""
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update fields
    update_data = job_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)
    
    db.commit()
    db.refresh(job)
    return job


@router.post("/{job_id}/retry", response_model=ProcessingJobResponse)
async def retry_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Retry a failed processing job"""
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != JobStatus.FAILED:
        raise HTTPException(status_code=400, detail="Only failed jobs can be retried")
    
    job_service = JobService(db)
    return await job_service.retry_job(job)


@router.post("/{job_id}/finalize")
async def finalize_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Finalize a processing job"""
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Only completed jobs can be finalized")
    
    job.is_finalized = True
    db.commit()
    
    return {"message": "Job finalized successfully"}


@router.get("/export/json")
async def export_json(
    finalized_only: bool = Query(True, description="Export only finalized jobs"),
    db: Session = Depends(get_db)
):
    """Export jobs as JSON"""
    query = db.query(ProcessingJob)
    
    if finalized_only:
        query = query.filter(ProcessingJob.is_finalized == True)
    
    jobs = query.all()
    
    # Prepare export data
    export_data = []
    for job in jobs:
        export_data.append({
            "id": job.id,
            "document_filename": job.document.original_filename,
            "status": job.status.value,
            "extracted_title": job.extracted_title,
            "extracted_category": job.extracted_category,
            "extracted_summary": job.extracted_summary,
            "extracted_keywords": job.extracted_keywords,
            "processed_content": job.processed_content,
            "final_result": job.final_result,
            "created_at": job.created_at.isoformat(),
            "completed_at": job.completed_at.isoformat() if job.completed_at else None
        })
    
    # Create JSON response
    json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
    
    return StreamingResponse(
        StringIO(json_data),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=jobs_export.json"}
    )


@router.get("/export/csv")
async def export_csv(
    finalized_only: bool = Query(True, description="Export only finalized jobs"),
    db: Session = Depends(get_db)
):
    """Export jobs as CSV"""
    query = db.query(ProcessingJob)
    
    if finalized_only:
        query = query.filter(ProcessingJob.is_finalized == True)
    
    jobs = query.all()
    
    # Create CSV data
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "ID", "Document Filename", "Status", "Title", "Category", 
        "Summary", "Keywords", "Created At", "Completed At"
    ])
    
    # Data rows
    for job in jobs:
        writer.writerow([
            job.id,
            job.document.original_filename,
            job.status.value,
            job.extracted_title or "",
            job.extracted_category or "",
            job.extracted_summary or "",
            ";".join(job.extracted_keywords) if job.extracted_keywords else "",
            job.created_at.isoformat(),
            job.completed_at.isoformat() if job.completed_at else ""
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        StringIO(output.getvalue()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=jobs_export.csv"}
    )
