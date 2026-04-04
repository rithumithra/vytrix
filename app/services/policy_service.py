from sqlalchemy.orm import Session
from app.models.policy import Policy
from app.models.user import UserProfile
from app.models.enums import CoverageType, PolicyStatus, PaymentFrequency, GeographicArea
from app.schemas.policy_schemas import PremiumCalculationResponse
from datetime import datetime, timedelta
import uuid


class PolicyService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_premium(
        self, 
        user_id: str, 
        coverage_type: CoverageType,
        zone: GeographicArea
    ) -> PremiumCalculationResponse:
        """Calculate premium for insurance coverage"""
        
        # Get user profile
        user = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Base premium calculation
        base_premium = self._get_base_premium(coverage_type)
        
        # Zone risk adjustment
        zone_risk_adjustment = self._calculate_zone_risk_adjustment(zone, base_premium)
        
        # Weather risk adjustment (simulated based on zone)
        weather_risk_adjustment = self._calculate_weather_risk_adjustment(zone, base_premium)
        
        # User-specific risk adjustment
        user_risk_adjustment = self._calculate_user_risk_adjustment(user, base_premium)
        
        # Calculate final premium
        final_premium = (
            base_premium + 
            zone_risk_adjustment + 
            weather_risk_adjustment + 
            user_risk_adjustment
        )
        
        # Ensure premium stays within bounds
        final_premium = max(100, min(300, final_premium))
        
        # Coverage amount (up to 10x premium)
        coverage_amount = final_premium * 10
        
        # Risk factors breakdown
        risk_factors = {
            "zone_risk": zone_risk_adjustment / base_premium,
            "weather_risk": weather_risk_adjustment / base_premium,
            "user_risk": user.risk_score,
            "vehicle_risk": self._get_vehicle_risk_factor(user.vehicle_type)
        }
        
        return PremiumCalculationResponse(
            base_premium=base_premium,
            zone_risk_adjustment=zone_risk_adjustment,
            weather_risk_adjustment=weather_risk_adjustment,
            final_premium=final_premium,
            coverage_amount=coverage_amount,
            coverage_type=coverage_type,
            risk_factors=risk_factors
        )

    def create_policy(
        self, 
        user_id: str, 
        coverage_type: CoverageType, 
        premium_amount: float
    ) -> Policy:
        """Create and activate insurance policy"""
        
        # Get user profile
        user = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Check for existing active policy
        existing_policy = self.db.query(Policy).filter(
            Policy.user_id == user_id,
            Policy.status == PolicyStatus.ACTIVE
        ).first()
        
        if existing_policy:
            raise ValueError("User already has an active policy")
        
        # Calculate coverage amount
        coverage_amount = premium_amount * 10
        
        # Set policy dates (weekly coverage)
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=7)
        
        # Create policy
        policy = Policy(
            policy_id=str(uuid.uuid4()),
            user_id=user_id,
            coverage_type=coverage_type,
            premium_amount=premium_amount,
            coverage_amount=coverage_amount,
            start_date=start_date,
            end_date=end_date,
            status=PolicyStatus.ACTIVE,
            payment_frequency=PaymentFrequency.WEEKLY,
            terms_conditions="Standard Vytrix insurance terms and conditions apply."
        )
        
        # Validate policy
        if not policy.validate_premium_amount():
            raise ValueError("Premium amount must be between ₹100-₹300")
        
        if not policy.validate_coverage_amount():
            raise ValueError("Coverage amount exceeds maximum allowed")
        
        if not policy.validate_dates():
            raise ValueError("Invalid policy dates")
        
        # Save to database
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        
        return policy

    def _get_base_premium(self, coverage_type: CoverageType) -> float:
        """Get base premium based on coverage type"""
        base_premiums = {
            CoverageType.LUNCH_PEAK: 150.0,
            CoverageType.DINNER_PEAK: 180.0,
            CoverageType.FULL_SHIFT: 250.0
        }
        return base_premiums.get(coverage_type, 200.0)

    def _calculate_zone_risk_adjustment(self, zone: GeographicArea, base_premium: float) -> float:
        """Calculate zone-based risk adjustment"""
        high_risk_zones = [
            GeographicArea.MUMBAI_CENTRAL,
            GeographicArea.DELHI_CENTRAL,
            GeographicArea.BANGALORE_CENTRAL
        ]
        
        medium_risk_zones = [
            GeographicArea.MUMBAI_NORTH,
            GeographicArea.MUMBAI_SOUTH,
            GeographicArea.DELHI_NORTH,
            GeographicArea.DELHI_SOUTH,
            GeographicArea.BANGALORE_NORTH,
            GeographicArea.BANGALORE_SOUTH
        ]
        
        if zone in high_risk_zones:
            return base_premium * 0.15  # 15% increase
        elif zone in medium_risk_zones:
            return base_premium * 0.10  # 10% increase
        else:
            return base_premium * 0.05   # 5% increase

    def _calculate_weather_risk_adjustment(self, zone: GeographicArea, base_premium: float) -> float:
        """Calculate weather-based risk adjustment"""
        # Simulated weather risk based on zone
        weather_risk_zones = {
            GeographicArea.MUMBAI_CENTRAL: 0.08,  # High monsoon risk
            GeographicArea.MUMBAI_NORTH: 0.08,
            GeographicArea.MUMBAI_SOUTH: 0.08,
            GeographicArea.MUMBAI_EAST: 0.08,
            GeographicArea.MUMBAI_WEST: 0.08,
            GeographicArea.DELHI_CENTRAL: 0.06,   # Moderate weather risk
            GeographicArea.DELHI_NORTH: 0.06,
            GeographicArea.DELHI_SOUTH: 0.06,
            GeographicArea.DELHI_EAST: 0.06,
            GeographicArea.DELHI_WEST: 0.06,
            GeographicArea.BANGALORE_CENTRAL: 0.04,  # Lower weather risk
            GeographicArea.BANGALORE_NORTH: 0.04,
            GeographicArea.BANGALORE_SOUTH: 0.04,
            GeographicArea.BANGALORE_EAST: 0.04,
            GeographicArea.BANGALORE_WEST: 0.04,
        }
        
        risk_factor = weather_risk_zones.get(zone, 0.05)
        return base_premium * risk_factor

    def _calculate_user_risk_adjustment(self, user: UserProfile, base_premium: float) -> float:
        """Calculate user-specific risk adjustment"""
        # Risk adjustment based on user's risk score
        risk_adjustment = (user.risk_score - 0.5) * base_premium * 0.2
        return risk_adjustment

    def _get_vehicle_risk_factor(self, vehicle_type) -> float:
        """Get risk factor based on vehicle type"""
        vehicle_risks = {
            "bicycle": 0.8,    # Higher risk
            "bike": 0.5,       # Medium risk
            "scooter": 0.4,    # Lower risk
            "car": 0.2         # Lowest risk
        }
        return vehicle_risks.get(vehicle_type.value, 0.5)

    def get_active_policy(self, user_id: str) -> Policy:
        """Get user's active policy"""
        policy = self.db.query(Policy).filter(
            Policy.user_id == user_id,
            Policy.status == PolicyStatus.ACTIVE
        ).first()
        
        if not policy:
            raise ValueError("No active policy found for user")
        
        return policy