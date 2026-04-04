from sqlalchemy.orm import Session
from app.models.claim import FraudAssessment
from app.models.opportunity_loss import OpportunityLossScore
import uuid
import random
from datetime import datetime


class FraudDetectionService:
    def __init__(self, db: Session):
        self.db = db

    def assess_fraud_risk(
        self, 
        opportunity_loss_score: OpportunityLossScore,
        scenario_type: str = "normal"
    ) -> FraudAssessment:
        """Assess fraud risk for a claim"""
        
        # Calculate fraud risk score based on scenario
        if scenario_type == "fraud":
            risk_score = self._calculate_high_fraud_risk()
            risk_level = "HIGH"
            fraud_indicators = [
                "GPS anomaly detected - impossible speed",
                "Location jump detected - >50km instant",
                "Activity not correlated with peer data",
                "Suspicious behavioral pattern"
            ]
            recommendation = "REJECT"
        elif scenario_type == "rain":
            risk_score = self._calculate_low_fraud_risk()
            risk_level = "LOW"
            fraud_indicators = []
            recommendation = "APPROVE"
        elif scenario_type == "no_activity":
            risk_score = self._calculate_medium_fraud_risk()
            risk_level = "MEDIUM"
            fraud_indicators = [
                "Extended stationary period detected",
                "No delivery attempts during shift"
            ]
            recommendation = "REVIEW"
        else:  # normal scenario
            risk_score = self._calculate_low_fraud_risk()
            risk_level = "LOW"
            fraud_indicators = []
            recommendation = "APPROVE"
        
        # Create fraud assessment
        fraud_assessment = FraudAssessment(
            assessment_id=str(uuid.uuid4()),
            claim_id=f"claim_{opportunity_loss_score.session_id}",
            risk_score=risk_score,
            risk_level=risk_level,
            fraud_indicators=", ".join(fraud_indicators) if fraud_indicators else None,
            recommendation=recommendation
        )
        
        # Validate assessment
        if not fraud_assessment.validate_risk_score():
            raise ValueError("Invalid fraud risk score")
        
        if not fraud_assessment.validate_risk_level():
            raise ValueError("Invalid fraud risk level")
        
        if not fraud_assessment.validate_recommendation():
            raise ValueError("Invalid fraud recommendation")
        
        # Save to database
        self.db.add(fraud_assessment)
        self.db.commit()
        self.db.refresh(fraud_assessment)
        
        return fraud_assessment

    def _calculate_high_fraud_risk(self) -> float:
        """Calculate high fraud risk score (0.7-1.0)"""
        return random.uniform(0.7, 1.0)

    def _calculate_medium_fraud_risk(self) -> float:
        """Calculate medium fraud risk score (0.4-0.6)"""
        return random.uniform(0.4, 0.6)

    def _calculate_low_fraud_risk(self) -> float:
        """Calculate low fraud risk score (0.0-0.3)"""
        return random.uniform(0.0, 0.3)

    def detect_gps_anomalies(self, gps_data: list) -> list:
        """Detect GPS anomalies in tracking data"""
        anomalies = []
        
        # Simulate GPS anomaly detection
        for i in range(len(gps_data) - 1):
            current_point = gps_data[i]
            next_point = gps_data[i + 1]
            
            # Calculate speed between points (simplified)
            time_diff = (next_point['timestamp'] - current_point['timestamp']).total_seconds()
            if time_diff > 0:
                # Simplified distance calculation (not accurate for real GPS)
                lat_diff = abs(next_point['latitude'] - current_point['latitude'])
                lon_diff = abs(next_point['longitude'] - current_point['longitude'])
                distance = (lat_diff + lon_diff) * 111  # Rough km conversion
                
                speed = distance / (time_diff / 3600)  # km/h
                
                if speed > 100:  # Impossible speed for delivery vehicles
                    anomalies.append({
                        "type": "IMPOSSIBLE_SPEED",
                        "severity": min(1.0, speed / 200),
                        "details": f"Speed: {speed:.1f} km/h"
                    })
                
                if distance > 50 and time_diff < 300:  # >50km in <5 minutes
                    anomalies.append({
                        "type": "LOCATION_JUMP",
                        "severity": min(1.0, distance / 100),
                        "details": f"Distance: {distance:.1f} km in {time_diff:.0f} seconds"
                    })
        
        return anomalies

    def analyze_behavioral_patterns(self, user_id: str, current_behavior: dict) -> dict:
        """Analyze user behavioral patterns for anomalies"""
        # Simulate behavioral analysis
        historical_avg_deliveries = random.randint(15, 25)
        current_deliveries = current_behavior.get('deliveries', 0)
        
        deviation_score = abs(current_deliveries - historical_avg_deliveries) / historical_avg_deliveries
        
        return {
            "deviation_score": min(1.0, deviation_score),
            "historical_average": historical_avg_deliveries,
            "current_value": current_deliveries,
            "is_anomalous": deviation_score > 0.7
        }

    def cross_reference_peers(self, user_activity: dict, peer_data: dict) -> dict:
        """Cross-reference user activity with peer data"""
        # Simulate peer comparison
        peer_avg_activity = peer_data.get('average_activity', 0.5)
        user_activity_level = user_activity.get('activity_level', 0.0)
        
        correlation_score = 1.0 - abs(peer_avg_activity - user_activity_level)
        
        return {
            "correlation_score": max(0.0, correlation_score),
            "peer_average": peer_avg_activity,
            "user_activity": user_activity_level,
            "is_correlated": correlation_score > 0.3
        }