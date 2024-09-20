from fastapi import FastAPI, Depends, Query, HTTPException
from typing import List, Optional
from auth import authenticate_token
from models import Job
from db import get_jobs_count, get_jobs
from scheduler import start_scheduler

# Create FastAPI app
app = FastAPI(title="Job Scraper API", version="1.0", docs_url="/api/docs")

# Routes
@app.get("/api/jobs", response_model=List[Job])
async def get_jobs_endpoint(
    token: str = Depends(authenticate_token),
    skip: int = 0,
    limit: int = 10,
    skill: Optional[str] = Query(None, description="Filter jobs by skill")
):
    jobs = await get_jobs(skip=skip, limit=limit, skill=skill)
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found")
    return jobs

@app.get("/api/metrics")
async def get_metrics():
    total_jobs = await get_jobs_count()
    return {"total_jobs_scraped": total_jobs, "status": "running"}

# Start job scheduler for scraping
start_scheduler()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
