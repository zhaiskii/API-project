from pydantic import BaseModel

# Job model for API response validation
class Job(BaseModel):
    id: int
    title: str
    skills: str
    date_posted: str
    link: str
