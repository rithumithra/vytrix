from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


class OpportunityLossScore(Base):
    __tablename__ = "opportunity_loss_scores"
    
    score_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user_profiles.user_id"), nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    
    # Individual Score Components (0.0 to 1.0)
    weather_score = Column(Float, nullable=False, default=0.0)  # 30% weight
    activity_drop_score = Column(Float, nullable=False, default=0.0)  # 20% weight
    movement_score = Column(Float, nullable=False, default=0.0)  # 20% weight
    peer_comparison_score = Column(Float, nullable=False, default=0.0)  # 15% weight
    behavioral_score = Column(Float, nullable=False, default=0.0)  # 15% weight
    
    # Composite Score and Threshold
    composite_score = Column(Float, nullable=False, default=0.0)  # Weighted average
    threshold = Column(Float, nullable=False, default=0.7)  # Dynamic threshold for payout
    
    # Timestamp
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("UserProfile", backref="opportunity_loss_scores")
    
    def __repr__(self):
        return f"<OpportunityLossScore(score_id={self.score_id}, composite_score={self.composite_score})>"
    
    def calculate_composite_score(self) -> float:
        """Calculate weighted composite score from individual components"""
        composite = (
            self.weather_score * 0.3 +
            self.activity_drop_score * 0.2 +
            self.movement_score * 0.2 +
            self.peer_comparison_score * 0.15 +
            self.behavioral_score * 0.15
        )
        self.composite_score = min(max(composite, 0.0), 1.0)  # Ensure bounds [0.0, 1.0]
        return self.composite_score
    
    def exceeds_threshold(self) -> bool:
        """Check if composite score exceeds threshold for claim approval"""
        return self.composite_score > self.threshold
    
    def validate_individual_scores(self) -> bool:
        """Validate all individual scores are within bounds [0.0, 1.0]"""
        scores = [
            self.weather_score,
            self.activity_drop_score,
            self.movement_score,
            self.peer_comparison_score,
            self.behavioral_score
        ]
        return all(0.0 <= score <= 1.0 for score in scores)
    
    def validate_composite_score(self) -> bool:
        """Validate composite score is within bounds and matches calculation"""
        expected_composite = (
            self.weather_score * 0.3 +
            self.activity_drop_score * 0.2 +
            self.movement_score * 0.2 +
            self.peer_comparison_score * 0.15 +
            self.behavioral_score * 0.15
        )
        return (
            0.0 <= self.composite_score <= 1.0 and
            abs(self.composite_score - expected_composite) < 0.001
        )
    
    def validate_threshold(self) -> bool:
        """Validate threshold is positive and reasonable"""
        return 0.0 < self.threshold <= 1.0
    
    def get_score_breakdown(self) -> dict:
        """Get detailed breakdown of score components"""
        return {
            "weather": {
                "score": self.weather_score,
                "weight": 0.3,
                "contribution": self.weather_score * 0.3
            },
            "activity_drop": {
                "score": self.activity_drop_score,
                "weight": 0.2,
                "contribution": self.activity_drop_score * 0.2
            },
            "movement": {
                "score": self.movement_score,
                "weight": 0.2,
                "contribution": self.movement_score * 0.2
            },
            "peer_comparison": {
                "score": self.peer_comparison_score,
                "weight": 0.15,
                "contribution": self.peer_comparison_score * 0.15
            },
            "behavioral": {
                "score": self.behavioral_score,
                "weight": 0.15,
                "contribution": self.behavioral_score * 0.15
            },
            "composite_score": self.composite_score,
            "threshold": self.threshold,
            "exceeds_threshold": self.exceeds_threshold()
        }