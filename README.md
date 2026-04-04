# vytrix - AI-Powered Income Protection for Gig Workers
# Problem Statement: AI-Powered Insurance for India’s Gig Economy
India’s platform-based delivery partners (such as Zomato, Swiggy, Zepto, Amazon, and Dunzo) form the backbone of the country’s fast-growing digital economy. These workers depend on daily deliveries for their income, making their earnings highly sensitive to external conditions.

However, disruptions such as extreme weather (heavy rain, heatwaves), high pollution levels, natural disasters, and sudden curfews can significantly reduce their ability to work. As a result, gig workers often experience a 20–30% loss in monthly income.

Currently, there is no structured or automated system to protect delivery workers from such uncontrollable income loss. When these disruptions occur, workers are forced to bear the entire financial burden without any safety net.

Additionally, existing approaches are highly vulnerable to fraudulent claims, such as GPS spoofing and false reporting.

Therefore, there is a need for an intelligent, automated and fraud-resistant income protection system.
---
# Objective
To build an AI-powered parametric insurance platform that:
* Detects real-world disruptions
* Evaluates actual income loss
* Automatically triggers payouts
* Prevents fraudulent claims
---
## Target Persona
Urban food delivery workers (e.g., Swiggy/Zomato riders).
----
# Persona-Based Scenario
Persona: Pravallika, 24, Swiggy delivery partner

Daily Income: ₹600

Scenario:During heavy rainfall, Pravallika is unable to complete deliveries for several hours. This results in direct income loss, with no compensation or support system.

---
# Solution Overview

Vytrix is an AI-powered parametric income protection platform designed for urban food delivery workers. Instead of relying only on weather alerts, the platform checks whether a real external disruption actually caused measurable income loss during the worker’s active earning hours.
## 1. Opportunity Loss Score
Vytrix introduces an Opportunity Loss Score, a composite metric that estimates whether a delivery partner genuinely lost earning opportunity due to a covered disruption. Rather than paying out simply because heavy rain or poor air quality occurred, the system evaluates whether the event actually reduced the worker’s ability to complete deliveries during their active shift.

The score is calculated using multiple signals such as:
* weather severity in the worker’s zone(30%)
* drop in delivery activity compared to normal patterns(20%)
* movement slowdown or stoppage during active hours(20%)
* nearby worker patterns in the same micro-zone(15%)
* behavioral consistency during the disruption period(15%)
# Decision:
If Opportunity Loss Score exceeds a threshold → payout is triggered automatically.

## 2. Shift-Aware Micro-Coverage
Food delivery earnings are usually concentrated during peak windows such as lunch and dinner. Instead of forcing every worker into the same broad coverage model, Vytrix offers flexible weekly protection options based on actual work patterns:
* Lunch Peak Cover
* Dinner Peak Cover
* Full Shift Cover
This allows workers to choose protection for the hours they depend on most. A worker who mainly earns during dinner hours can pay for dinner-only protection instead of paying for full-day coverage they do not need. This makes the product more affordable, personalized and aligned with real gig work.
---
# Application Workflow
1.Worker signs up and selects delivery zone, preferred shift

2.Worker subscribes to a weekly plan

3.System continuously monitors:
   * Weather conditions
   * Worker activity (simulated)
   * Movement patterns

4.Opportunity Loss Score is calculated

5.If threshold exceeded:
   * Claim is auto-triggered
   * Fraud checks applied
   * Payout simulated
6.Upon successful verification, payout is processed (simulated)
---

## System Workflow

The following diagram represents the end-to-end automated workflow of Vytrix, from user onboarding to claim decision and payout.

![Workflow Diagram](./workflow.png)


# Weekly Pricing Model
Premium is calculated on a weekly basis based on:
* Area risk level
* Historical weather data
* Worker activity patterns
In return, the worker receives one week of income-loss protection against verified external disruptions such as heavy rain, hazardous AQI, extreme heat or restricted zones. If a covered event causes genuine opportunity loss and the worker passes fraud validation, the system automatically triggers a payout up to the plan’s defined limit.
# Example:

* Low Risk: ₹100/week
* Medium Risk: ₹200/week
* High Risk: ₹300/week
---

# Insurance Design & Compliance
Coverage Conditions (All must be satisfied):

* Worker active during insured shift
* Disruption exceeds threshold
        (Rain > 20 mm/hr, AQI > 300, Temp > 40°C)
* Activity drop ≥ 50% vs baseline
* Opportunity Loss Score > 0.7

Exclusions (No payout if):

* Inactive before disruption
* No delivery attempts during shift
* GPS spoofing / device tampering detected
* App offline / tracking disabled
* No actual disruption in micro-zone

Payout Limit:
* Max = 50% of avg daily earnings
(e.g., ₹600 → ₹300)

Compliance Note:
* Follows parametric insurance model (predefined triggers, transparent payouts)
* Extendable to regulatory sandbox frameworks

# Parametric Triggers
* Heavy rainfall above threshold
* Hazardous AQI levels
* Extreme temperatures
* Curfews or restricted zones
---
# Platform Choice (Web vs Mobile)
We propose a Mobile-first approach because:
* Delivery workers primarily use smartphones
* Real-time tracking and notifications are easier
* Better accessibility during working hours
* Supports future use of live device signals such as GPS continuity, motion data and real-time alerts.

## Local Postgres and Deployment Setup
### Use local PostgreSQL for development
1. Start the backend services with Docker Compose:
   ```bash
   docker compose up -d postgres redis influxdb
   ```
2. The app now supports a `config.json` file at the repo root, so you do not need to manually create a full `DATABASE_URL`.
   - A default `config.json` is already provided with local Postgres values.
   - The app will use that file if `DATABASE_URL` is not set.
3. Optionally, create a `.env` file in the repo root for secrets or overrides:
   ```env
   # only needed if you want to override defaults
   DATABASE_URL=postgresql://vytrix_user:vytrix_password@localhost:5432/vytrix_db
   REDIS_URL=redis://localhost:6379/0
   INFLUXDB_URL=http://localhost:8086
   INFLUXDB_TOKEN=vytrix-super-secret-auth-token
   INFLUXDB_ORG=vytrix
   ```
4. Run the app using the virtualenv and the `.env` file:
   ```bash
   source venv/bin/activate
   python run.py
   ```

### Use a deployed PostgreSQL database
- In production, set `DATABASE_URL` to your managed Postgres connection string.
- Example:
  ```env
  DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<dbname>
  ```
- Do not rely on the default SQLite URL for deployed environments.
- Services like Heroku, Render, Railway, or any cloud provider will provide a database URL you can paste into `DATABASE_URL`.

### Notes
- The app first reads `.env` and environment variables using Pydantic BaseSettings.
- If `DATABASE_URL` is not set, the app will build the connection URL from `config.json`.
- If `config.json` is absent, the app falls back to local Postgres defaults.

## AI/ML Integration
# 1. Risk Prediction
A supervised learning model (e.g., regression/classification) estimates disruption probability for each micro-zone

Inputs:
* Historical weather patterns
* Seasonal trends
* Zone-specific disruption frequency

Output:
Risk score used to dynamically adjust weekly premium

Example: Higher flood-prone zones → higher premium
# 2. Opportunity Loss Evaluation
A multi-factor weighted scoring system evaluates real income loss

Combines:
* Environmental signals (weather severity, AQI)
* Behavioral signals (activity drop, movement slowdown)
* Contextual signals (peer activity in same zone)

Can be extended to:
* Time-series anomaly detection (detect abnormal drop vs normal pattern)
* Personalized baseline modeling for each worker

Output:
Opportunity Loss Score → used for claim triggering
# 3.Fraud Detection
Uses unsupervised / semi-supervised models to detect abnormal behavior
Key Techniques:
* GPS anomaly detection
    Detects sudden jumps, unrealistic movement patterns
* Behavioral anomaly detection
    Compares current activity vs historical user behavior
* Peer comparison model
    Cross-validates claims using nearby worker activity
* Device signal validation
    Motion sensor + network consistency checks
In the prototype, this is implemented using a rule-based fraud scoring system with scope to evolve into adaptive models.
# 4. Trust Score System (Reputation Model)
* Each user is assigned a dynamic trust score

Based on:
* Claim history
* Fraud flags
* Behavioral consistency
Used for:
* Faster approval (high trust users)
* Strict validation (low trust users)
# 5. Real-Time Decision Engine
Combines outputs from:
* Risk model
* Opportunity loss model
* Fraud detection system
Final decision:
* Approve claim
* Flag for review
* Reject
---
# Adversarial Defense & Anti-Spoofing Strategy
# Problem:
Workers may attempt to exploit the system using GPS spoofing or fake claims.
# Our Approach:
# 1. DIFFERENTIATION : Real vs Spoofed Users
GENUINE:
* Continuous movement (road-based)
* Realistic speed patterns
* Activity drop during disruption
* Network instability

SPOOFED:
* Sudden jumps / static location
* No deliveries
* Perfect GPS but no motion
* No history consistency
# 2. Data : Multi-Signal Validation
* Location: GPS + cell tower
* Device: motion (accelerometer)
* Network: IP + latency
* Behavior: activity vs baseline
* Environment: weather API
* Peer: nearby worker activity
# 3. Fraud Detection Logic (Prototype Implementation)
fraud_score = 0

if gps_jump: fraud_score += 0.4

if no_movement: fraud_score += 0.3

if peer_mismatch: fraud_score += 0.3

Decision:
* `< 0.3 → Approve`
* `0.3–0.6 → Verify`
* `> 0.6 → Under Review` 
# 4. Coordinated Fraud Detection
Detects clusters of users with:
 * same claim time
 * similar behavior
 * no movement
→ Flag as Suspicious Cluster
# 5. Explainability
System shows why decision was made:
 * Rain > threshold
 * Activity drop > 60%
 * Peer inactivity confirmed

----
# Tech Stack
**Frontend:**
* HTML / CSS / React (basic UI)
**Backend:**
* Python (Flask)
**AI/ML:**
* Prototype stage uses rule-based scoring and simulated AI logic , with scope to evolve into trained ML models in later phases.
**APIs:**
* Weather API (or mock data)
* Mock activity data
* Mock payment system
---
# Key Features
* Opportunity Loss Score
* Behavior-based payout system
* Automated claim triggering
* Fraud detection (peer + trust model)
* Weekly subscription model
---
# Phase 1 
* Idea design
* README documentation
* UI prototype
# Phase 2:
Core functionality (registration, premium calculation, claims)
# Phase 3:
* Fraud detection improvements
* Dashboard and analytics
---

# Conclusion
Vytrix provides a smart, automated, and fraud-resistant solution to protect gig workers from income loss. By combining behavioral intelligence with parametric triggers, it ensures fair and timely compensation in real-world conditions.The system evolves from a rule-based prototype to an adaptive, data-driven model with dynamic thresholds and learning-based fraud detection.
---
