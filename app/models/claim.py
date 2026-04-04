from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import ClaimStatus
import uuid


class ClaimData(Base):
    __tablename__ = "claims"
    
    claim_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user_profiles.user_id"), nullable=False, index=True)
    policy_id = Column(String, ForeignKey("policies.policy_id"), nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    opportunity_loss_score_id = Column(String, ForeignKey("opportunity_loss_scores.score_id"), nullable=True)
    
    # Claim Details
    claim_amount = Column(Float, nullable=False)  # Requested payout amount in INR
    status = Column(SQLEnum(ClaimStatus), default=ClaimStatus.PENDING)
    reason = Column(Text, nullable=True)  # Reason for approval/rejection
    
    # Processing Information
    processed_at = Column(DateTime(timezone=True), nullable=True)
    payout_reference = Column(String, nullable=True)  # Payment gateway reference
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("UserProfile", backref="claims")
    policy = relationship("Policy", backref="claims")
    opportunity_loss_score = relationship("OpportunityLossScore", backref="claims")
    
    def __repr__(self):
        return f"<ClaimData(claim_id={self.claim_id}, status={self.status}, amount={self.claim_amount})>"
    
    @property
    def is_pending(self) -> bool:
        """Check if claim is still pending processing"""
        return self.status == ClaimStatus.PENDING
    
    @property
    def is_approved(self) -> bool:
        """Check if claim has been approved"""
        return self.status == ClaimStatus.APPROVED
    
    @property
    def is_paid(self) -> bool:
        """Check if claim has been paid out"""
        return self.status == ClaimStatus.PAID
    
    def validate_claim_amount(self) -> bool:
        """Validate claim amount doesn't exceed policy coverage"""
        if not self.policy:
            return False
        return self.claim_amount <= self.policy.coverage_amount
    
    def validate_processing_requirements(self) -> bool:
        """Validate claim has required data for processing"""
        return (
            self.user_id is not None and
            self.policy_id is not None and
            self.session_id is not None and
            self.claim_amount > 0
        )
    
    def can_be_processed(self) -> bool:
        """Check if claim can be processed"""
        return (
            self.is_pending and
            self.validate_claim_amount() and
            self.validate_processing_requirements()
        )


class FraudAssessment(Base):
    __tablename__ = "fraud_assessments"
    
    assessment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id = Column(String, ForeignKey("claims.claim_id"), nullable=False, index=True)
    
    # Fraud Risk Assessment
    risk_score = Column(Float, nullable=False, default=0.0)  # 0.0 to 1.0
    risk_level = Column(String, nullable=False)  # LOW, MEDIUM, HIGH
    fraud_indicators = Column(Text, nullable=True)  # JSON string of fraud indicators
    recommendation = Column(String, nullable=False)  # APPROVE, REVIEW, REJECT
    
    # Timestamp
    assessed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    claim = relationship("ClaimData", backref="fraud_assessments")
    
    def __repr__(self):
        return f"<FraudAssessment(assessment_id={self.assessment_id}, risk_level={self.risk_level})>"
    
    def validate_risk_score(self) -> bool:
        """Validate risk score is within bounds"""
        return 0.0 <= self.risk_score <= 1.0
    
    def validate_risk_level(self) -> bool:
        """Validate risk level is valid"""
        return self.risk_level in ["LOW", "MEDIUM", "HIGH"]
    
    def validate_recommendation(self) -> bool:
        """Validate recommendation is valid"""
        return self.recommendation in ["APPROVE", "REVIEW", "REJECT"]
    
    def should_approve(self) -> bool:
        """Check if assessment recommends approval"""
        return self.recommendation == "APPROVE" and self.risk_level != "HIGH"
    
    def should_reject(self) -> bool:
        """Check if assessment recommends rejection"""
        return self.recommendation == "REJECT" or self.risk_level == "HIGH"