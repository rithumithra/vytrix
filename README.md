# 🛡️ Vytrix Insurance Platform

**AI-Powered Parametric Insurance for Gig Workers**

A comprehensive insurance platform that provides real-time, data-driven coverage for delivery partners using advanced opportunity loss scoring and fraud detection algorithms.

## 🚀 Features

### 🎯 **Core Functionality**
- **User Registration & Verification** - Seamless onboarding for gig workers
- **Dynamic Premium Calculation** - Risk-based pricing with zone and weather adjustments
- **Real-time Claim Processing** - Instant decision making with AI-powered scoring
- **Multi-scenario Simulation** - Test different claim scenarios (Rain, Fraud, No Activity)

### 🧠 **AI/ML Capabilities**
- **Opportunity Loss Scoring** - Weighted algorithm considering weather, activity, movement, peer data, and behavioral patterns
- **Fraud Detection** - Multi-signal analysis with GPS anomaly detection and behavioral pattern recognition
- **Risk Assessment** - Dynamic threshold calculation based on user profiles

### 📱 **User Experience**
- **Mobile-First Design** - Responsive React frontend optimized for mobile devices
- **Intuitive Workflow** - Registration → Premium → Activation → Claims
- **Real-time Results** - Instant claim decisions with detailed reasoning

## 🏗️ Architecture

### **Backend (FastAPI + SQLAlchemy)**
```
app/
├── models/          # Database models (User, Policy, Claims, etc.)
├── schemas/         # Pydantic validation schemas
├── services/        # Business logic (Scoring, Fraud Detection, etc.)
├── main.py         # FastAPI application and routes
├── database.py     # Database configuration
└── config.py       # Application settings
```

### **Frontend (React)**
```
frontend/
├── src/
│   ├── components/  # React components (Registration, Premium, etc.)
│   ├── App.js      # Main application
│   └── index.css   # Styling
└── package.json    # Dependencies
```

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.8+
- Node.js 14+
- npm or yarn

### **Backend Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd vytrix-insurance-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python run.py
```

### **Frontend Setup**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

### **Quick Start Script**
```bash
# Make the script executable
chmod +x start-frontend.sh

# Start both backend and frontend
./start-frontend.sh
```

## 🧪 Testing

### **Test Scenarios**
The platform includes 5 comprehensive test scenarios:

1. **🌧️ Heavy Rain Storm** - Legitimate weather claim (₹400 payout)
2. **⚠️ Fraudulent Claim** - Fraud detection test (₹0 payout)
3. **📵 No Activity** - Manual review process (₹0 pending)
4. **🌦️ Multiple Rain Tests** - Consistency validation
5. **🔄 Cross-Platform** - Platform independence testing

See `test_scenarios.md` for detailed testing instructions.

### **API Testing**
```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","phone_number":"9876543210","delivery_platform":"swiggy","vehicle_type":"bike","primary_work_area":"bangalore_central","average_daily_earnings":600}'

# Test rain scenario
curl -X POST "http://localhost:8000/api/simulate/rain" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"YOUR_USER_ID"}'
```

## 📊 Scoring Algorithm

### **Opportunity Loss Score Components**
- **Weather Impact (30%)** - Rain, temperature, wind conditions
- **Activity Drop (20%)** - Delivery activity reduction
- **Movement Patterns (20%)** - GPS-based movement analysis
- **Peer Comparison (15%)** - Activity correlation with other workers
- **Behavioral Analysis (15%)** - Historical pattern analysis

### **Fraud Detection Signals**
- GPS anomaly detection (impossible speeds, location jumps)
- Activity pattern inconsistencies
- Peer data correlation analysis
- Behavioral deviation scoring

## 🎯 Expected Results

| Scenario | Status | Opportunity Score | Fraud Score | Claim Amount |
|----------|--------|------------------|-------------|--------------|
| Rain Storm | APPROVED ✅ | 0.75+ | 0.1-0.3 | ₹400 |
| Fraud Attempt | REJECTED ❌ | 0.2-0.4 | 0.7-1.0 | ₹0 |
| No Activity | UNDER_REVIEW ⏳ | 0.5-0.7 | 0.4-0.6 | ₹0* |

*₹250 if approved after manual review

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file (optional):
```env
DATABASE_URL=sqlite:///./vytrix.db
SECRET_KEY=your-secret-key
DEBUG=True
```

### **Database**
The platform uses SQLite by default for simplicity. Database tables are created automatically on first run.

## 📱 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🚀 Deployment

### **Production Considerations**
- Use PostgreSQL instead of SQLite
- Configure proper CORS settings
- Set up environment variables
- Enable HTTPS
- Implement proper logging
- Add monitoring and alerting

### **Docker Support** (Optional)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React for the frontend framework
- SQLAlchemy for database ORM
- Pydantic for data validation

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the `test_scenarios.md` for troubleshooting

---

**Built with ❤️ for the gig economy workers**