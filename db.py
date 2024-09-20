import sqlite3
from typing import List, Optional
from models import Job

# SQLite connection (asynchronous)
conn = sqlite3.connect('job_scraper.db', check_same_thread=False)
c = conn.cursor()

# Initialize jobs table
def init_db():
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            skills TEXT,
            date_posted TEXT,
            link TEXT
        )
    """)
    conn.commit()

# Get total job count
async def get_jobs_count() -> int:
    query = 'SELECT COUNT(*) FROM jobs'
    c.execute(query)
    return c.fetchone()[0]

# Get jobs with pagination and optional filtering
async def get_jobs(skip: int, limit: int, skill: Optional[str]) -> List[Job]:
    query = 'SELECT * FROM jobs'
    params = []

    if skill:
        query += ' WHERE skills LIKE ?'
        params.append(f"%{skill}%")

    query += ' LIMIT ? OFFSET ?'
    params.extend([limit, skip])

    c.execute(query, params)
    jobs = c.fetchall()
    return [Job(id=job[0], title=job[1], skills=job[2], date_posted=job[3], link=job[4]) for job in jobs]
