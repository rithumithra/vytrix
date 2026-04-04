from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "service": "vytrix-flask"})

@app.route('/api/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    # Mock registration
    return jsonify({"message": "User registered", "user": data})

@app.route('/api/policies/calculate-premium', methods=['POST'])
def calculate_premium():
    data = request.get_json()
    # Mock premium calculation
    return jsonify({"premium": 100.0, "details": "Mock calculation"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)