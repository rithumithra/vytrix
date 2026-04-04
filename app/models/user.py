from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import DeliveryPlatform, VehicleType, GeographicArea, VerificationStatus
import uuid


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)
    
    # Delivery Platform Information
    delivery_platform = Column(SQLEnum(DeliveryPlatform), nullable=False)
    vehicle_type = Column(SQLEnum(VehicleType), nullable=False)
    primary_work_area = Column(SQLEnum(GeographicArea), nullable=False)
    
    # Financial and Risk Information
    average_daily_earnings = Column(Float, nullable=False)  # In INR
    risk_score = Column(Float, nullable=False, default=0.5)  # 0.0 to 1.0
    
    # Verification Status
    verification_status = Column(SQLEnum(VerificationStatus), default=VerificationStatus.PENDING)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, name={self.name}, phone={self.phone_number})>"
    
    @property
    def is_verified(self) -> bool:
        return self.verification_status == VerificationStatus.VERIFIED
    
    def validate_phone_number(self) -> bool:
        """Validate Indian mobile number format"""
        if not self.phone_number:
            return False
        # Remove any non-digit characters
        digits_only = ''.join(filter(str.isdigit, self.phone_number))
        # Check if it's 10 digits and starts with valid prefixes
        if len(digits_only) == 10 and digits_only[0] in ['6', '7', '8', '9']:
            return True
        return False
    
    def validate_earnings(self) -> bool:
        """Validate daily earnings are within expected range"""
        return 200 <= self.average_daily_earnings <= 2000
    
    def validate_risk_score(self) -> bool:
        """Validate risk score is within bounds"""
        return 0.0 <= self.risk_score <= 1.0