"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# CRM-focused schemas for the freelancing agency

class Lead(BaseModel):
    """
    Leads captured from the website contact form
    Collection name: "lead"
    """
    name: str = Field(..., description="Full name of the prospect")
    email: EmailStr = Field(..., description="Contact email")
    company: Optional[str] = Field(None, description="Company or organization")
    phone: Optional[str] = Field(None, description="Phone number")
    budget: Optional[str] = Field(None, description="Estimated budget range")
    timeline: Optional[str] = Field(None, description="Desired timeline")
    service: Optional[str] = Field(None, description="Service interested in")
    message: Optional[str] = Field(None, description="Project description or message")
    source: str = Field("website", description="Lead source identifier")
    status: str = Field("new", description="Lead status: new, contacted, qualified, proposal, won, lost")

class Project(BaseModel):
    """
    Portfolio projects shown on the website
    Collection name: "project"
    """
    title: str
    description: str
    tags: List[str] = []
    url: Optional[str] = None
    image: Optional[str] = None
    highlight: bool = False

class Testimonial(BaseModel):
    """
    Client testimonials
    Collection name: "testimonial"
    """
    name: str
    role: Optional[str] = None
    quote: str
    avatar: Optional[str] = None

class Service(BaseModel):
    """
    Services offered
    Collection name: "service"
    """
    name: str
    description: str
    icon: Optional[str] = None

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!  
