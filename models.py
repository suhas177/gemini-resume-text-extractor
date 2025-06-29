# In your main.py or a models.py file
from pydantic import BaseModel, Field
from typing import List, Optional

class WorkExperience(BaseModel):
    company: Optional[str] = Field(None, description="Name of the company")
    role: Optional[str] = Field(None, description="Job title or role")
    start_date: Optional[str] = Field(None, description="Start date of employment")
    end_date: Optional[str] = Field(None, description="End date of employment (or 'Present')")
    description: Optional[str] = Field(None, description="Key responsibilities and achievements")

class Education(BaseModel):
    institution: Optional[str] = Field(None, description="Name of the university or school")
    degree: Optional[str] = Field(None, description="Degree obtained (e.g., Bachelor of Science)")
    field_of_study: Optional[str] = Field(None, description="Field of study (e.g., Computer Science)")
    graduation_date: Optional[str] = Field(None, description="Date of graduation")

class ResumeData(BaseModel):
    full_name: Optional[str] = Field(None, description="The full name of the candidate")
    email: Optional[str] = Field(None, description="The primary email address")
    phone_number: Optional[str] = Field(None, description="The contact phone number")
    linkedin_url: Optional[str] = Field(None, description="URL of the LinkedIn profile")
    summary: Optional[str] = Field(None, description="A professional summary or objective statement")
    skills: List[str] = Field([], description="A list of key skills")
    work_experience: List[WorkExperience] = Field([], description="A list of work experiences")
    education: List[Education] = Field([], description="A list of educational qualifications")