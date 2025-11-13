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

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List, Literal

# Core schemas for the Stray Animal Welfare app

class Animal(BaseModel):
    """
    Animals available for adoption or in shelter care
    Collection name: "animal"
    """
    name: str = Field(..., description="Animal name (if known)")
    species: Literal["dog", "cat", "bird", "other"] = Field(..., description="Species")
    age: Optional[str] = Field(None, description="Approximate age, e.g., '2 years' or '6 months'")
    gender: Optional[Literal["male", "female", "unknown"]] = Field("unknown", description="Gender if known")
    description: Optional[str] = Field(None, description="Temperament, health, etc.")
    status: Literal["adoptable", "rescued", "fostered", "medical", "other"] = Field("adoptable", description="Current status")
    location: Optional[str] = Field(None, description="City/Area")
    photo_url: Optional[HttpUrl] = Field(None, description="Public link to animal photo")

class Sighting(BaseModel):
    """
    Citizen-reported stray animal sightings
    Collection name: "sighting"
    """
    species: Literal["dog", "cat", "bird", "other"] = Field(..., description="Species seen")
    location_text: str = Field(..., description="Street/landmark/city")
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    notes: Optional[str] = Field(None, description="Behavior, condition, collar, etc.")
    reporter_name: Optional[str] = Field(None, description="Your name")
    reporter_contact: Optional[str] = Field(None, description="Phone or email")
    photo_url: Optional[HttpUrl] = Field(None, description="Photo link if available")
    status: Literal["new", "in_progress", "resolved"] = Field("new")
    urgency: Optional[Literal["low", "medium", "high"]] = Field("medium")

class Volunteer(BaseModel):
    """
    Volunteer sign-ups
    Collection name: "volunteer"
    """
    name: str
    email: EmailStr
    phone: Optional[str] = None
    areas_of_interest: List[str] = Field(default_factory=list, description="e.g., rescue, foster, transport, outreach")
    availability: Optional[str] = Field(None, description="Days/times available")
    notes: Optional[str] = None

class Donation(BaseModel):
    """
    Donation pledges or contact
    Collection name: "donation"
    """
    name: str
    email: Optional[EmailStr] = None
    amount: Optional[float] = Field(None, ge=0)
    message: Optional[str] = None
