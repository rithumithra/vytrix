from sqlalchemy.orm import Session
from app.models.opportunity_loss import OpportunityLossScore
from app.models.user import UserProfile
import uuid
import random
from datetime import datetime


class OpportunityLossService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_opportunity_loss_score(
        self, 
        user_id: str, 
        session_id: str,
        scenario_type: str = "normal"
    ) -> OpportunityLossScore:
        """Calculate opportunity loss score for a session"""
        
        # Get user profile
        user = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Calculate individual score components based on scenario
        if scenario_type == "rain":
            weather_score = self._calculate_rain_weather_score()
            activity_drop_score = self._calculate_rain_activity_score()
            movement_score = self._calculate_rain_movement_score()
            peer_comparison_score = self._calculate_rain_peer_score()
            behavioral_score = self._calculate_normal_behavioral_score(user)
        elif scenario_type == "fraud":
            weather_score = self._calculate_normal_weather_score()
            activity_drop_score = self._calculate_fraud_activity_score()
            movement_score = self._calculate_fraud_movement_score()
            peer_comparison_score = self._calculate_fraud_peer_score()
            behavioral_score = self._calculate_fraud_behavioral_score()
        elif scenario_type == "no_activity":
            weather_score = self._calculate_normal_weather_score()
            activity_drop_score = self._calculate_no_activity_score()
            movement_score = self._calculate_no_movement_score()
            peer_comparison_score = self._calculate_normal_peer_score()
            behavioral_score = self._calculate_normal_behavioral_score(user)
        else:  # normal scenario
            weather_score = self._calculate_normal_weather_score()
            activity_drop_score = self._calculate_normal_activity_score()
            movement_score = self._calculate_normal_movement_score()
            peer_comparison_score = self._calculate_normal_peer_score()
            behavioral_score = self._calculate_normal_behavioral_score(user)
        
        # Calculate dynamic threshold based on user profile
        threshold = self._calculate_dynamic_threshold(user)
        
        # Create opportunity loss score record
        opportunity_loss_score = OpportunityLossScore(
            score_id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            weather_score=weather_score,
            activity_drop_score=activity_drop_score,
            movement_score=movement_score,
            peer_comparison_score=peer_comparison_score,
            behavioral_score=behavioral_score,
            threshold=threshold
        )
        
        # Calculate composite score
        opportunity_loss_score.calculate_composite_score()
        
        # Validate scores
        if not opportunity_loss_score.validate_individual_scores():
            raise ValueError("Invalid individual scores calculated")
        
        if not opportunity_loss_score.validate_composite_score():
            raise ValueError("Invalid composite score calculated")
        
        if not opportunity_loss_score.validate_threshold():
            raise ValueError("Invalid threshold calculated")
        
        # Save to database
        self.db.add(opportunity_loss_score)
        self.db.commit()
        self.db.refresh(opportunity_loss_score)
        
        return opportunity_loss_score

    def _calculate_rain_weather_score(self) -> float:
        """Calculate weather score for rain scenario"""
        # Simulate heavy rain conditions - ensure high score
        return 0.9  # High weather impact for rain scenario

    def _calculate_rain_activity_score(self) -> float:
        """Calculate activity drop score for rain scenario"""
        # Simulate significant activity drop during rain - ensure high score
        return random.uniform(0.8, 0.95)

    def _calculate_rain_movement_score(self) -> float:
        """Calculate movement score for rain scenario"""
        # Simulate reduced movement during rain - ensure high score
        return random.uniform(0.7, 0.85)

    def _calculate_rain_peer_score(self) -> float:
        """Calculate peer comparison score for rain scenario"""
        # Simulate that peers also affected by rain - ensure high score
        return random.uniform(0.8, 0.95)

    def _calculate_fraud_activity_score(self) -> float:
        """Calculate activity score for fraud scenario"""
        # Simulate claimed activity drop but suspicious patterns - moderate score
        return random.uniform(0.5, 0.7)

    def _calculate_fraud_movement_score(self) -> float:
        """Calculate movement score for fraud scenario"""
        # Simulate suspicious movement patterns
        return random.uniform(0.1, 0.3)

    def _calculate_fraud_peer_score(self) -> float:
        """Calculate peer score for fraud scenario"""
        # Simulate peers showing normal activity
        return random.uniform(0.1, 0.3)

    def _calculate_fraud_behavioral_score(self) -> float:
        """Calculate behavioral score for fraud scenario"""
        # Simulate suspicious behavioral patterns
        return random.uniform(0.1, 0.3)

    def _calculate_no_activity_score(self) -> float:
        """Calculate activity score for no activity scenario"""
        # Simulate complete activity drop
        return 1.0

    def _calculate_no_movement_score(self) -> float:
        """Calculate movement score for no activity scenario"""
        # Simulate no movement
        return 1.0

    def _calculate_normal_weather_score(self) -> float:
        """Calculate normal weather score"""
        return random.uniform(0.1, 0.3)

    def _calculate_normal_activity_score(self) -> float:
        """Calculate normal activity score"""
        return random.uniform(0.2, 0.4)

    def _calculate_normal_movement_score(self) -> float:
        """Calculate normal movement score"""
        return random.uniform(0.2, 0.4)

    def _calculate_normal_peer_score(self) -> float:
        """Calculate normal peer score"""
        return random.uniform(0.4, 0.6)

    def _calculate_normal_behavioral_score(self, user: UserProfile) -> float:
        """Calculate normal behavioral score based on user profile"""
        # Base score influenced by user's risk profile
        base_score = 0.3
        risk_adjustment = (user.risk_score - 0.5) * 0.2
        return max(0.0, min(1.0, base_score + risk_adjustment))

    def _calculate_dynamic_threshold(self, user: UserProfile) -> float:
        """Calculate dynamic threshold based on user profile"""
        base_threshold = 0.7
        
        # Adjust based on user's risk score
        risk_adjustment = (user.risk_score - 0.5) * 0.1
        
        # Adjust based on verification status
        if user.verification_status.value == "verified":
            verification_adjustment = -0.05  # Lower threshold for verified users
        else:
            verification_adjustment = 0.05   # Higher threshold for unverified users
        
        threshold = base_threshold + risk_adjustment + verification_adjustment
        
        # Ensure threshold stays within reasonable bounds
        return max(0.3, min(0.8, threshold))