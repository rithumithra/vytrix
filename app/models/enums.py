from enum import Enum


class DeliveryPlatform(str, Enum):
    SWIGGY = "swiggy"
    ZOMATO = "zomato"
    ZEPTO = "zepto"
    AMAZON = "amazon"
    DUNZO = "dunzo"
    OTHER = "other"


class VehicleType(str, Enum):
    BIKE = "bike"
    SCOOTER = "scooter"
    BICYCLE = "bicycle"
    CAR = "car"


class GeographicArea(str, Enum):
    # Major Indian Cities
    BANGALORE_CENTRAL = "bangalore_central"
    BANGALORE_NORTH = "bangalore_north"
    BANGALORE_SOUTH = "bangalore_south"
    BANGALORE_EAST = "bangalore_east"
    BANGALORE_WEST = "bangalore_west"
    
    MUMBAI_CENTRAL = "mumbai_central"
    MUMBAI_NORTH = "mumbai_north"
    MUMBAI_SOUTH = "mumbai_south"
    MUMBAI_EAST = "mumbai_east"
    MUMBAI_WEST = "mumbai_west"
    
    DELHI_CENTRAL = "delhi_central"
    DELHI_NORTH = "delhi_north"
    DELHI_SOUTH = "delhi_south"
    DELHI_EAST = "delhi_east"
    DELHI_WEST = "delhi_west"
    
    HYDERABAD_CENTRAL = "hyderabad_central"
    CHENNAI_CENTRAL = "chennai_central"
    PUNE_CENTRAL = "pune_central"
    KOLKATA_CENTRAL = "kolkata_central"


class CoverageType(str, Enum):
    LUNCH_PEAK = "lunch_peak"  # 11 AM - 3 PM
    DINNER_PEAK = "dinner_peak"  # 6 PM - 10 PM
    FULL_SHIFT = "full_shift"  # 8 AM - 10 PM


class PolicyStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"


class ClaimStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"
    UNDER_REVIEW = "under_review"


class VerificationStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    DOCUMENTS_REQUIRED = "documents_required"


class PaymentFrequency(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ShiftType(str, Enum):
    LUNCH_PEAK = "lunch_peak"
    DINNER_PEAK = "dinner_peak"
    FULL_SHIFT = "full_shift"


class AnomalyType(str, Enum):
    IMPOSSIBLE_SPEED = "impossible_speed"
    LOCATION_JUMP = "location_jump"
    STATIONARY_PERIOD = "stationary_period"