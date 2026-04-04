from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.enums import CoverageType, PolicyStatus, GeographicArea


class PremiumCalculationRequest(BaseModel):
    user_id: str = Field(..., description="User ID for premium calculation")
    coverage_type: CoverageType = Field(..., description="Type of coverage requested")
    zone: GeographicArea = Field(..., description="Work zone for risk assessment")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "coverage_type": "dinner_peak",
                "zone": "bangalore_central"
            }
        }


class PremiumCalculationResponse(BaseModel):
    base_premium: float = Field(..., description="Base premium amount in INR")
    zone_risk_adjustment: float = Field(..., description="Zone-based risk adjustment in INR")
    weather_risk_adjustment: float = Field(..., description="Weather-based risk adjustment in INR")
    final_premium: float = Field(..., description="Final premium amount in INR")
    coverage_amount: float = Field(..., description="Maximum coverage amount in INR")
    coverage_type: CoverageType = Field(..., description="Type of coverage")
    risk_factors: dict = Field(..., description="Detailed risk factor breakdown")

    class Config:
        json_schema_extra = {
            "example": {
                "base_premium": 200.0,
                "zone_risk_adjustment": 20.0,
                "weather_risk_adjustment": 10.0,
                "final_premium": 230.0,
                "coverage_amount": 2300.0,
                "coverage_type": "dinner_peak",
                "risk_factors": {
                    "zone_risk": 0.1,
                    "weather_risk": 0.05,
                    "user_risk": 0.5,
                    "vehicle_risk": 0.2
                }
            }
        }


class PolicyActivationRequest(BaseModel):
    user_id: str = Field(..., description="User ID for policy activation")
    coverage_type: CoverageType = Field(..., description="Type of coverage to activate")
    premium_amount: float = Field(..., ge=100, le=300, description="Premium amount in INR")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "coverage_type": "dinner_peak",
                "premium_amount": 230.0
            }
        }


class PolicyResponse(BaseModel):
    policy_id: str
    user_id: str
    coverage_type: CoverageType
    premium_amount: float
    coverage_amount: float
    start_date: datetime
    end_date: datetime
    status: PolicyStatus
    created_at: datetime

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "policy_id": "policy_67890",
                "user_id": "user_12345",
                "coverage_type": "dinner_peak",
                "premium_amount": 230.0,
                "coverage_amount": 2300.0,
                "start_date": "2024-01-15T00:00:00Z",
                "end_date": "2024-01-22T00:00:00Z",
                "status": "active",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }