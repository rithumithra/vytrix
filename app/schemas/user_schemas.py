from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from app.models.enums import DeliveryPlatform, VehicleType, GeographicArea, VerificationStatus


class UserRegistrationRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the user")
    phone_number: str = Field(..., pattern=r"^[6-9]\d{9}$", description="10-digit Indian mobile number")
    delivery_platform: DeliveryPlatform = Field(..., description="Primary delivery platform")
    vehicle_type: VehicleType = Field(..., description="Vehicle used for deliveries")
    primary_work_area: GeographicArea = Field(..., description="Primary work zone")
    average_daily_earnings: float = Field(..., ge=200, le=2000, description="Average daily earnings in INR")
    email: Optional[str] = Field(None, description="Email address (optional)")

    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Phone number must be 10 digits')
        if not v.startswith(('6', '7', '8', '9')):
            raise ValueError('Phone number must start with 6, 7, 8, or 9')
        return v

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Rajesh Kumar",
                "phone_number": "9876543210",
                "delivery_platform": "swiggy",
                "vehicle_type": "bike",
                "primary_work_area": "bangalore_central",
                "average_daily_earnings": 600,
                "email": "rajesh@example.com"
            }
        }


class UserProfileResponse(BaseModel):
    user_id: str
    name: str
    phone_number: str
    email: Optional[str]
    delivery_platform: DeliveryPlatform
    vehicle_type: VehicleType
    primary_work_area: GeographicArea
    average_daily_earnings: float
    risk_score: float
    verification_status: VerificationStatus
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "name": "Rajesh Kumar",
                "phone_number": "9876543210",
                "email": "rajesh@example.com",
                "delivery_platform": "swiggy",
                "vehicle_type": "bike",
                "primary_work_area": "bangalore_central",
                "average_daily_earnings": 600.0,
                "risk_score": 0.5,
                "verification_status": "pending",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }