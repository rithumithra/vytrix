# 🧪 Vytrix Insurance Platform - Test Scenarios

## Overview
This document contains 5 comprehensive test scenarios to validate the Vytrix Insurance Platform's different claim outcomes and payout amounts.

---

## 📋 **Scenario 1: Heavy Rain Storm** 🌧️
**Expected Outcome: APPROVED with High Payout**

### Test Steps:
1. **Register User:**
   ```json
   {
     "name": "Rajesh Kumar",
     "phone_number": "9876543210",
     "delivery_platform": "swiggy",
     "vehicle_type": "bike",
     "primary_work_area": "bangalore_central",
     "average_daily_earnings": 600
   }
   ```

2. **Calculate Premium:** Should show ₹230 total
3. **Activate Policy**
4. **Trigger:** Click "Simulate Rain" button

### Expected Results:
- **Status:** APPROVED ✅
- **Opportunity Score:** 0.75+ (High)
- **Fraud Score:** 0.0-0.3 (Low)
- **Claim Amount:** ₹400
- **Reasons:** 
  - Rain > threshold
  - Activity drop 80%+
  - Peer activity correlation confirmed

---

## 📋 **Scenario 2: Fraudulent Claim Attempt** ⚠️
**Expected Outcome: REJECTED with No Payout**

### Test Steps:
1. **Register User:**
   ```json
   {
     "name": "Suspicious User",
     "phone_number": "8765432109",
     "delivery_platform": "zomato",
     "vehicle_type": "scooter",
     "primary_work_area": "mumbai_south",
     "average_daily_earnings": 800
   }
   ```

2. **Calculate Premium:** Should show ₹230 total
3. **Activate Policy**
4. **Trigger:** Click "Simulate Fraud" button

### Expected Results:
- **Status:** REJECTED ❌
- **Opportunity Score:** 0.2-0.4 (Low)
- **Fraud Score:** 0.7-1.0 (High)
- **Claim Amount:** ₹0
- **Reasons:**
  - GPS anomaly detected - impossible speed
  - Location jump detected - >50km instant
  - High fraud risk detected

---

## 📋 **Scenario 3: No Activity During Shift** 📵
**Expected Outcome: UNDER_REVIEW with Pending Payout**

### Test Steps:
1. **Register User:**
   ```json
   {
     "name": "Inactive Worker",
     "phone_number": "7654321098",
     "delivery_platform": "uber_eats",
     "vehicle_type": "bike",
     "primary_work_area": "delhi_north",
     "average_daily_earnings": 500
   }
   ```

2. **Calculate Premium:** Should show ₹230 total
3. **Activate Policy**
4. **Trigger:** Click "No Activity" button

### Expected Results:
- **Status:** UNDER_REVIEW ⏳
- **Opportunity Score:** 0.5-0.7 (Medium)
- **Fraud Score:** 0.4-0.6 (Medium)
- **Claim Amount:** ₹0 (Pending review, would be ₹250 if approved)
- **Reasons:**
  - Complete activity cessation detected
  - No movement during shift
  - Requires manual review

---

## 📋 **Scenario 4: Multiple Rain Tests** 🌦️
**Expected Outcome: Consistent APPROVED Results**

### Test Steps:
1. **Use the same user from Scenario 1**
2. **Test Rain scenario 3 times in a row**
3. **Compare results for consistency**

### Expected Results:
- **All 3 tests should show:** APPROVED status
- **Opportunity Scores:** Should vary between 0.75-0.85
- **Fraud Scores:** Should stay low (0.1-0.3)
- **Claim Amounts:** Should consistently be ₹400
- **Validation:** Randomness in scores but consistent outcomes

---

## 📋 **Scenario 5: Cross-Platform Comparison** 🔄
**Expected Outcome: Platform-Independent Results**

### Test Steps:
1. **Create 3 users with different platforms:**

   **User A - Swiggy:**
   ```json
   {
     "name": "Swiggy Rider",
     "phone_number": "9111111111",
     "delivery_platform": "swiggy",
     "vehicle_type": "bike",
     "primary_work_area": "chennai_central",
     "average_daily_earnings": 550
   }
   ```

   **User B - Zomato:**
   ```json
   {
     "name": "Zomato Partner",
     "phone_number": "9222222222",
     "delivery_platform": "zomato",
     "vehicle_type": "scooter",
     "primary_work_area": "hyderabad_west",
     "average_daily_earnings": 650
   }
   ```

   **User C - Uber Eats:**
   ```json
   {
     "name": "Uber Driver",
     "phone_number": "9333333333",
     "delivery_platform": "uber_eats",
     "vehicle_type": "bike",
     "primary_work_area": "pune_east",
     "average_daily_earnings": 700
   }
   ```

2. **Test Rain scenario for all 3 users**
3. **Compare results across platforms**

### Expected Results:
- **All 3 should get:** APPROVED status for rain
- **Slight variations in scores** due to different risk profiles
- **Consistent ₹400 payout** regardless of platform
- **Platform-agnostic claim processing**

---

## 🚀 **Quick Test Commands**

### Start the System:
```bash
# Terminal 1: Start Backend
source venv/bin/activate
python run.py

# Terminal 2: Start Frontend  
./start-frontend.sh
```

### API Testing (Alternative to UI):
```bash
# Register User
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","phone_number":"9876543210","delivery_platform":"swiggy","vehicle_type":"bike","primary_work_area":"bangalore_central","average_daily_earnings":600}'

# Test Rain (replace USER_ID)
curl -X POST "http://localhost:8000/api/simulate/rain" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"YOUR_USER_ID_HERE"}'

# Test Fraud
curl -X POST "http://localhost:8000/api/simulate/fraud" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"YOUR_USER_ID_HERE"}'

# Test No Activity
curl -X POST "http://localhost:8000/api/simulate/no-activity" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"YOUR_USER_ID_HERE"}'
```

---

## 📊 **Expected Payout Summary**

| Scenario | Status | Opportunity Score | Fraud Score | Claim Amount |
|----------|--------|------------------|-------------|--------------|
| Rain Storm | APPROVED ✅ | 0.75+ | 0.1-0.3 | ₹400 |
| Fraud Attempt | REJECTED ❌ | 0.2-0.4 | 0.7-1.0 | ₹0 |
| No Activity | UNDER_REVIEW ⏳ | 0.5-0.7 | 0.4-0.6 | ₹0* |
| Multiple Rain | APPROVED ✅ | 0.75-0.85 | 0.1-0.3 | ₹400 |
| Cross-Platform | APPROVED ✅ | 0.75+ | 0.1-0.3 | ₹400 |

*₹250 if approved after manual review

---

## 🎯 **Success Criteria**

✅ **Rain scenarios consistently get APPROVED with ₹400 payout**  
✅ **Fraud scenarios consistently get REJECTED with ₹0 payout**  
✅ **No activity scenarios go to UNDER_REVIEW**  
✅ **Different platforms produce similar results for same scenario**  
✅ **Scores show appropriate randomness while maintaining logical outcomes**

---

## 🐛 **Troubleshooting**

**If all scenarios return same result:**
- Check if server restarted after code changes
- Verify database has test users
- Check console for any errors

**If frontend doesn't connect:**
- Ensure backend is running on port 8000
- Check CORS settings in main.py
- Verify frontend is on port 3000

**If API calls fail:**
- Check user_id format (should be UUID)
- Verify JSON payload structure
- Check server logs for detailed errors