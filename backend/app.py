import pickle
model = pickle.load(open("model.pkl", "rb"))
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import requests
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random

# Load env
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
CORS(app)

# -----------------------------
# 📧 MAIL CONFIG (SYSTEM EMAIL)
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vytrixapp@gmail.com'      # 🔥 your gmail
app.config['MAIL_PASSWORD'] = 'cxfh lndl pzhj pyay'        # 🔥 app password

mail = Mail(app)

# -----------------------------
# DB CONFIG
# -----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vytrix.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# 🔥 OTP STORE
# -----------------------------
otp_store = {}

# -----------------------------
# 👤 USER TABLE
# -----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    trust_score = db.Column(db.Integer, default=50)

# -----------------------------
# 📄 PROFILE TABLE
# -----------------------------
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    zone = db.Column(db.String(50))
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    earnings = db.Column(db.Float)

# -----------------------------
# 📊 CLAIM TABLE
# -----------------------------
class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    opportunity_score = db.Column(db.Float)
    fraud_score = db.Column(db.Float)
    decision = db.Column(db.String(20))
    payout = db.Column(db.Float)
    rain = db.Column(db.Float)
    temp = db.Column(db.Float)
    
    
    

# -----------------------------
# 🌧 WEATHER
# -----------------------------
def get_weather(city):
    try:
        if not city or city == "Select City":
            return {"rain": 0, "temp": 30}

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()

        print("API RESPONSE:", data)

        if data.get("cod") != 200:
            return {"rain": 0, "temp": 30}

        return {
            "rain": data.get("rain", {}).get("1h", 0),
            "temp": data["main"]["temp"]
        }

    except Exception as e:
        print("Weather error:", e)
        return {"rain": 0, "temp": 30}
# 🤖 SCORE
# -----------------------------
def ai_opportunity_model(weather):
    rain = weather["rain"]
    temp = weather["temp"]
    activity = 0.6

    w = model["weights"]
    b = model["bias"]

    score = (
        rain * w["rain"] +
        temp * w["temp"] / 50 +
        activity * w["activity"] +
        b
    )

    # normalize
    score = max(0, min(1, score))

    return round(score, 2)
# -----------------------------
# 🚫 FRAUD
# -----------------------------
def fraud_score():
    score = 0
    if random.choice([0,1]): score += 0.5
    if random.choice([0,1]): score += 0.3
    if random.choice([0,1]): score += 0.2
    return round(score,2)

# =========================================================
# 🔐 OTP FLOW
# =========================================================

# SEND OTP
@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data["email"]

    otp = str(random.randint(1000, 9999))
    otp_store[email] = otp

    print("OTP:", otp)   # ✅ SAFE

    return jsonify({
    "message": "OTP sent",
    "otp": otp
})

# VERIFY OTP → CREATE ACCOUNT
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json

    email = data["email"]
    otp = data["otp"]

    if otp_store.get(email) == otp:

        user = User(
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            password=data["password"]
        )

        db.session.add(user)
        db.session.commit()

        otp_store.pop(email)

        return jsonify({"status": "success"})

    else:
        return jsonify({"status": "fail"})

# =========================================================
# 🔐 LOGIN (EMAIL + PASSWORD)
# =========================================================

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(
        email=data["email"],
        password=data["password"]
    ).first()

    if user:
        return jsonify({
            "status": "success",
            "user_id": user.id,
            "trust_score": user.trust_score
        })
    else:
        return jsonify({"status": "fail"})

# =========================================================
# 📄 PROFILE
# =========================================================

@app.route('/create_profile', methods=['POST'])
def create_profile():
    data = request.json

    profile = Profile(
        user_id=data["user_id"],
        zone=data["zone"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        earnings=data["earnings"]
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "Profile created"})

# =========================================================
# 📊 CLAIM
# =========================================================

@app.route('/claim', methods=['POST'])
def claim():
    data = request.json
    user_id = data["user_id"]

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 400

    weather = {"rain": 10, "temp": 38}

    opp = ai_opportunity_model(weather)
    fraud = 0.2

    if opp > 0.4 and fraud < 0.5:
        decision = "APPROVED"
        payout = profile.earnings * 0.5
    elif fraud < 0.6:
        decision = "VERIFY"
        payout = 0
    else:
        decision = "REJECTED"
        payout = 0

    claim = Claim(
        user_id=user_id,
        opportunity_score=opp,
        fraud_score=fraud,
        decision=decision,
        payout=payout,
        rain=weather["rain"],
        temp=weather["temp"]
    )

    db.session.add(claim)
    user = User.query.get(user_id)

    if decision == "APPROVED":
        user.trust_score += 10
    elif decision == "VERIFY":
        user.trust_score += 2
    elif decision == "REJECTED":
        user.trust_score -= 10
    db.session.commit()

    return jsonify({
    "weather": weather,
    "opportunity_score": opp,
    "fraud_score": fraud,
    "decision": decision,
    "payout": payout,
    
    # 🔥 ADD THIS
    "transaction_id": f"TXN{random.randint(10000,99999)}"
})
        
    

# =========================================================
# 📜 HISTORY
# =========================================================

@app.route('/history/<int:user_id>')
def history(user_id):
    claims = Claim.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "score": c.opportunity_score,
            "decision": c.decision,
            "payout": c.payout
        } for c in claims
    ])

# =========================================================
@app.route('/debug')
def debug():
    users = User.query.all()
    return jsonify([u.email for u in users])

import threading
import time

def auto_monitor():
    with app.app_context():
        while True:
            profiles = Profile.query.all()

            for p in profiles:
                weather = get_weather(p.zone)

                opp = calculate_score(weather)
                fraud = fraud_score()

                if opp > 0.7 and fraud < 0.3:
                    print(f"🚀 AUTO CLAIM for user {p.user_id} | payout: {p.earnings * 0.5}")

            time.sleep(60)  # every 1 minute



if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True)


