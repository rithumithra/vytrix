from sqlalchemy.orm import Session
from app.services.opportunity_loss_service import OpportunityLossService
from app.services.fraud_detection_service import FraudDetectionService
from app.services.policy_service import PolicyService
from app.schemas.simulation_schemas import SimulationResultResponse
import uuid
from datetime import datetime


class SimulationService:
    def __init__(self, db: Session):
        self.db = db
        self.opportunity_loss_service = OpportunityLossService(db)
        self.fraud_detection_service = FraudDetectionService(db)
        self.policy_service = PolicyService(db)

    def simulate_rain_scenario(self, user_id: str, session_id: str = None) -> SimulationResultResponse:
        """Simulate rain scenario with high opportunity loss, low fraud risk"""
        
        if not session_id:
            session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        # Calculate opportunity loss score for rain scenario
        opportunity_score = self.opportunity_loss_service.calculate_opportunity_loss_score(
            user_id=user_id,
            session_id=session_id,
            scenario_type="rain"
        )
        
        # Assess fraud risk for rain scenario
        fraud_assessment = self.fraud_detection_service.assess_fraud_risk(
            opportunity_loss_score=opportunity_score,
            scenario_type="rain"
        )
        
        # Determine claim status
        status = self._determine_claim_status(opportunity_score, fraud_assessment)
        
        # Generate reasons
        reasons = self._generate_reasons(opportunity_score, fraud_assessment, "rain")
        
        # Calculate claim amount if approved
        claim_amount = None
        if status == "APPROVED":
            try:
                policy = self.policy_service.get_active_policy(user_id)
                claim_amount = min(policy.coverage_amount, policy.coverage_amount * 0.6)  # Max 60% of coverage for rain
            except ValueError:
                claim_amount = 400.0  # Higher amount for rain scenario
        
        return SimulationResultResponse(
            session_id=session_id,
            opportunity_score=opportunity_score.composite_score,
            fraud_score=fraud_assessment.risk_score,
            status=status,
            threshold=opportunity_score.threshold,
            reasons=reasons,
            score_breakdown=opportunity_score.get_score_breakdown(),
            claim_amount=claim_amount,
            processed_at=datetime.utcnow()
        )

    def simulate_fraud_scenario(self, user_id: str, session_id: str = None) -> SimulationResultResponse:
        """Simulate fraud scenario with suspicious patterns"""
        
        if not session_id:
            session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        # Calculate opportunity loss score for fraud scenario
        opportunity_score = self.opportunity_loss_service.calculate_opportunity_loss_score(
            user_id=user_id,
            session_id=session_id,
            scenario_type="fraud"
        )
        
        # Assess fraud risk for fraud scenario
        fraud_assessment = self.fraud_detection_service.assess_fraud_risk(
            opportunity_loss_score=opportunity_score,
            scenario_type="fraud"
        )
        
        # Determine claim status
        status = self._determine_claim_status(opportunity_score, fraud_assessment)
        
        # Generate reasons
        reasons = self._generate_reasons(opportunity_score, fraud_assessment, "fraud")
        
        return SimulationResultResponse(
            session_id=session_id,
            opportunity_score=opportunity_score.composite_score,
            fraud_score=fraud_assessment.risk_score,
            status=status,
            threshold=opportunity_score.threshold,
            reasons=reasons,
            score_breakdown=opportunity_score.get_score_breakdown(),
            claim_amount=None,  # No payout for fraud
            processed_at=datetime.utcnow()
        )

    def simulate_no_activity_scenario(self, user_id: str, session_id: str = None) -> SimulationResultResponse:
        """Simulate no activity scenario"""
        
        if not session_id:
            session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        # Calculate opportunity loss score for no activity scenario
        opportunity_score = self.opportunity_loss_service.calculate_opportunity_loss_score(
            user_id=user_id,
            session_id=session_id,
            scenario_type="no_activity"
        )
        
        # Assess fraud risk for no activity scenario
        fraud_assessment = self.fraud_detection_service.assess_fraud_risk(
            opportunity_loss_score=opportunity_score,
            scenario_type="no_activity"
        )
        
        # Determine claim status
        status = self._determine_claim_status(opportunity_score, fraud_assessment)
        
        # Generate reasons
        reasons = self._generate_reasons(opportunity_score, fraud_assessment, "no_activity")
        
        # Calculate claim amount if approved
        claim_amount = None
        if status == "APPROVED":
            try:
                policy = self.policy_service.get_active_policy(user_id)
                claim_amount = min(policy.coverage_amount, policy.coverage_amount * 0.4)  # Max 40% for no activity
            except ValueError:
                claim_amount = 250.0  # Lower amount for no activity scenario
        
        return SimulationResultResponse(
            session_id=session_id,
            opportunity_score=opportunity_score.composite_score,
            fraud_score=fraud_assessment.risk_score,
            status=status,
            threshold=opportunity_score.threshold,
            reasons=reasons,
            score_breakdown=opportunity_score.get_score_breakdown(),
            claim_amount=claim_amount,
            processed_at=datetime.utcnow()
        )

    def _determine_claim_status(self, opportunity_score, fraud_assessment) -> str:
        """Determine claim status based on scores and fraud assessment"""
        
        # High fraud risk always results in rejection
        if fraud_assessment.risk_level == "HIGH":
            return "REJECTED"
        
        # Medium fraud risk goes to manual review
        if fraud_assessment.risk_level == "MEDIUM":
            return "UNDER_REVIEW"
        
        # Low fraud risk with high opportunity loss score gets approved
        if (fraud_assessment.risk_level == "LOW" and 
            opportunity_score.composite_score > opportunity_score.threshold):
            return "APPROVED"
        
        # Otherwise rejected
        return "REJECTED"

    def _generate_reasons(self, opportunity_score, fraud_assessment, scenario_type: str) -> list:
        """Generate reasons for claim decision"""
        reasons = []
        
        if scenario_type == "rain":
            if opportunity_score.weather_score > 0.5:
                reasons.append("Rain > threshold")
            if opportunity_score.activity_drop_score > 0.6:
                reasons.append(f"Activity drop {int(opportunity_score.activity_drop_score * 100)}%")
            if opportunity_score.peer_comparison_score > 0.6:
                reasons.append("Peer activity correlation confirmed")
            if opportunity_score.composite_score > opportunity_score.threshold:
                reasons.append("Opportunity loss score exceeds threshold")
        
        elif scenario_type == "fraud":
            if fraud_assessment.fraud_indicators:
                fraud_list = fraud_assessment.fraud_indicators.split(", ")
                reasons.extend(fraud_list[:2])  # Show first 2 fraud indicators
            reasons.append("High fraud risk detected")
        
        elif scenario_type == "no_activity":
            if opportunity_score.activity_drop_score > 0.8:
                reasons.append("Complete activity cessation detected")
            if opportunity_score.movement_score > 0.8:
                reasons.append("No movement during shift")
            if fraud_assessment.risk_level == "MEDIUM":
                reasons.append("Requires manual review")
        
        return reasons if reasons else ["Standard processing completed"]