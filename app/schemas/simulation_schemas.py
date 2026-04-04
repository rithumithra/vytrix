from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SimulationRequest(BaseModel):
    user_id: str = Field(..., description="User ID for simulation")
    session_id: Optional[str] = Field(None, description="Session ID (auto-generated if not provided)")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "session_id": "session_67890"
            }
        }


class SimulationResultResponse(BaseModel):
    session_id: str = Field(..., description="Session ID for the simulation")
    opportunity_score: float = Field(..., description="Calculated opportunity loss score (0.0-1.0)")
    fraud_score: float = Field(..., description="Calculated fraud risk score (0.0-1.0)")
    status: str = Field(..., description="Claim status (APPROVED/REJECTED/UNDER_REVIEW)")
    threshold: float = Field(..., description="Dynamic threshold for approval")
    reasons: List[str] = Field(..., description="List of reasons for the decision")
    score_breakdown: dict = Field(..., description="Detailed breakdown of score components")
    claim_amount: Optional[float] = Field(None, description="Claim amount if approved")
    processed_at: datetime = Field(..., description="Processing timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_67890",
                "opportunity_score": 0.78,
                "fraud_score": 0.12,
                "status": "APPROVED",
                "threshold": 0.7,
                "reasons": [
                    "Rain > threshold",
                    "Activity drop 65%",
                    "Peer activity correlation confirmed"
                ],
                "score_breakdown": {
                    "weather": {
                        "score": 0.8,
                        "weight": 0.3,
                        "contribution": 0.24
                    },
                    "activity_drop": {
                        "score": 0.9,
                        "weight": 0.2,
                        "contribution": 0.18
                    },
                    "movement": {
                        "score": 0.7,
                        "weight": 0.2,
                        "contribution": 0.14
                    },
                    "peer_comparison": {
                        "score": 0.8,
                        "weight": 0.15,
                        "contribution": 0.12
                    },
                    "behavioral": {
                        "score": 0.6,
                        "weight": 0.15,
                        "contribution": 0.09
                    }
                },
                "claim_amount": 300.0,
                "processed_at": "2024-01-15T14:30:00Z"
            }
        }