from sqlalchemy.orm import Session
from app.models.user import UserProfile
from app.models.enums import VerificationStatus
from app.schemas.user_schemas import UserRegistrationRequest
import uuid


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_data: UserRegistrationRequest) -> UserProfile:
        """Register a new gig worker user"""
        
        # Check if user already exists
        existing_user = self.db.query(UserProfile).filter(
            UserProfile.phone_number == user_data.phone_number
        ).first()
        
        if existing_user:
            raise ValueError("User with this phone number already exists")
        
        # Calculate initial risk score based on user data
        initial_risk_score = self._calculate_initial_risk_score(user_data)
        
        # Create new user profile
        user_profile = UserProfile(
            user_id=str(uuid.uuid4()),
            phone_number=user_data.phone_number,
            name=user_data.name,
            email=user_data.email,
            delivery_platform=user_data.delivery_platform,
            vehicle_type=user_data.vehicle_type,
            primary_work_area=user_data.primary_work_area,
            average_daily_earnings=user_data.average_daily_earnings,
            risk_score=initial_risk_score,
            verification_status=VerificationStatus.PENDING
        )
        
        # Validate user data
        if not user_profile.validate_phone_number():
            raise ValueError("Invalid phone number format")
        
        if not user_profile.validate_earnings():
            raise ValueError("Daily earnings must be between ₹200-₹2000")
        
        if not user_profile.validate_risk_score():
            raise ValueError("Invalid risk score calculation")
        
        # Save to database
        self.db.add(user_profile)
        self.db.commit()
        self.db.refresh(user_profile)
        
        return user_profile

    def _calculate_initial_risk_score(self, user_data: UserRegistrationRequest) -> float:
        """Calculate initial risk score based on user registration data"""
        risk_score = 0.5  # Base risk score
        
        # Zone-based risk adjustment
        high_risk_zones = [
            "mumbai_central", "delhi_central", "bangalore_central"
        ]
        if user_data.primary_work_area.value in high_risk_zones:
            risk_score += 0.1
        
        # Vehicle-based risk adjustment
        if user_data.vehicle_type.value == "bicycle":
            risk_score += 0.1  # Higher risk for bicycle riders
        elif user_data.vehicle_type.value == "car":
            risk_score -= 0.1  # Lower risk for car drivers
        
        # Earnings-based risk adjustment
        if user_data.average_daily_earnings < 400:
            risk_score += 0.1  # Higher risk for lower earnings
        elif user_data.average_daily_earnings > 800:
            risk_score -= 0.1  # Lower risk for higher earnings
        
        # Platform-based risk adjustment
        established_platforms = ["swiggy", "zomato"]
        if user_data.delivery_platform.value in established_platforms:
            risk_score -= 0.05  # Slightly lower risk for established platforms
        
        # Ensure risk score stays within bounds
        return max(0.0, min(1.0, risk_score))

    def get_user_by_id(self, user_id: str) -> UserProfile:
        """Get user by ID"""
        user = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")
        return user

    def get_user_by_phone(self, phone_number: str) -> UserProfile:
        """Get user by phone number"""
        user = self.db.query(UserProfile).filter(
            UserProfile.phone_number == phone_number
        ).first()
        if not user:
            raise ValueError("User not found")
        return user

    def update_risk_score(self, user_id: str, new_risk_score: float) -> UserProfile:
        """Update user's risk score"""
        user = self.get_user_by_id(user_id)
        
        if not (0.0 <= new_risk_score <= 1.0):
            raise ValueError("Risk score must be between 0.0 and 1.0")
        
        user.risk_score = new_risk_score
        self.db.commit()
        self.db.refresh(user)
        
        return user