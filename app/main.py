from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import *
from app.schemas import *
from app.services import *
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vytrix Insurance Platform",
    description="AI-powered parametric insurance for gig workers",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Vytrix Insurance Platform API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "vytrix-api"}

# User Registration Endpoint
@app.post("/api/users/register", response_model=UserProfileResponse)
async def register_user(
    user_data: UserRegistrationRequest,
    db: Session = Depends(get_db)
):
    """Register a new gig worker user"""
    try:
        user_service = UserService(db)
        user_profile = user_service.register_user(user_data)
        return user_profile
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")

# Premium Calculation Endpoint
@app.post("/api/policies/calculate-premium", response_model=PremiumCalculationResponse)
async def calculate_premium(
    request: PremiumCalculationRequest,
    db: Session = Depends(get_db)
):
    """Calculate premium for insurance coverage"""
    try:
        policy_service = PolicyService(db)
        premium_details = policy_service.calculate_premium(
            user_id=request.user_id,
            coverage_type=request.coverage_type,
            zone=request.zone
        )
        return premium_details
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Premium calculation failed")

# Policy Activation Endpoint
@app.post("/api/policies/activate", response_model=PolicyResponse)
async def activate_policy(
    request: PolicyActivationRequest,
    db: Session = Depends(get_db)
):
    """Activate insurance policy"""
    try:
        policy_service = PolicyService(db)
        policy = policy_service.create_policy(
            user_id=request.user_id,
            coverage_type=request.coverage_type,
            premium_amount=request.premium_amount
        )
        return policy
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Policy activation failed")

# Simulation Endpoints for Testing
@app.post("/api/simulate/rain", response_model=SimulationResultResponse)
async def simulate_rain(
    request: SimulationRequest,
    db: Session = Depends(get_db)
):
    """Simulate rain scenario for testing"""
    try:
        simulation_service = SimulationService(db)
        result = simulation_service.simulate_rain_scenario(
            user_id=request.user_id,
            session_id=request.session_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Simulation failed")

@app.post("/api/simulate/fraud", response_model=SimulationResultResponse)
async def simulate_fraud(
    request: SimulationRequest,
    db: Session = Depends(get_db)
):
    """Simulate fraud scenario for testing"""
    try:
        simulation_service = SimulationService(db)
        result = simulation_service.simulate_fraud_scenario(
            user_id=request.user_id,
            session_id=request.session_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Simulation failed")

@app.post("/api/simulate/no-activity", response_model=SimulationResultResponse)
async def simulate_no_activity(
    request: SimulationRequest,
    db: Session = Depends(get_db)
):
    """Simulate no activity scenario for testing"""
    try:
        simulation_service = SimulationService(db)
        result = simulation_service.simulate_no_activity_scenario(
            user_id=request.user_id,
            session_id=request.session_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Simulation failed")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)