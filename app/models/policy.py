from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import CoverageType, PolicyStatus, PaymentFrequency
import uuid


class Policy(Base):
    __tablename__ = "policies"
    
    policy_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user_profiles.user_id"), nullable=False, index=True)
    
    # Coverage Details
    coverage_type = Column(SQLEnum(CoverageType), nullable=False)
    premium_amount = Column(Float, nullable=False)  # Weekly premium in INR
    coverage_amount = Column(Float, nullable=False)  # Maximum payout amount in INR
    
    # Policy Lifecycle
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(SQLEnum(PolicyStatus), default=PolicyStatus.PENDING)
    payment_frequency = Column(SQLEnum(PaymentFrequency), default=PaymentFrequency.WEEKLY)
    
    # Terms and Conditions
    terms_conditions = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("UserProfile", backref="policies")
    
    def __repr__(self):
        return f"<Policy(policy_id={self.policy_id}, user_id={self.user_id}, coverage_type={self.coverage_type})>"
    
    @property
    def is_active(self) -> bool:
        """Check if policy is currently active"""
        from datetime import datetime
        now = datetime.utcnow()
        return (
            self.status == PolicyStatus.ACTIVE and
            self.start_date <= now <= self.end_date
        )
    
    def validate_premium_amount(self) -> bool:
        """Validate premium is within acceptable range"""
        return 100 <= self.premium_amount <= 300
    
    def validate_coverage_amount(self) -> bool:
        """Validate coverage amount doesn't exceed 10x premium"""
        return self.coverage_amount <= (self.premium_amount * 10)
    
    def validate_dates(self) -> bool:
        """Validate end date is after start date"""
        return self.end_date > self.start_date
    
    def get_coverage_hours(self) -> tuple:
        """Get coverage hours based on coverage type"""
        coverage_hours = {
            CoverageType.LUNCH_PEAK: (11, 15),  # 11 AM - 3 PM
            CoverageType.DINNER_PEAK: (18, 22),  # 6 PM - 10 PM
            CoverageType.FULL_SHIFT: (8, 22)     # 8 AM - 10 PM
        }
        return coverage_hours.get(self.coverage_type, (8, 22))