import React, { useState } from 'react';
import axios from 'axios';

const RegistrationPage = ({ onSuccess, onLoading, onError }) => {
  const [formData, setFormData] = useState({
    name: '',
    phone_number: '',
    zone: '',
    shift: '',
    delivery_platform: '',
    vehicle_type: '',
    average_daily_earnings: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    onLoading();

    try {
      // Register user
      const userResponse = await axios.post('/api/users/register', {
        name: formData.name,
        phone_number: formData.phone_number,
        delivery_platform: formData.delivery_platform,
        vehicle_type: formData.vehicle_type,
        primary_work_area: formData.zone,
        average_daily_earnings: parseFloat(formData.average_daily_earnings)
      });

      const userData = userResponse.data;

      // Calculate premium
      const premiumResponse = await axios.post('/api/policies/calculate-premium', {
        user_id: userData.user_id,
        coverage_type: formData.shift,
        zone: formData.zone
      });

      const premiumData = premiumResponse.data;

      onSuccess(userData, premiumData);
    } catch (error) {
      console.error('Registration error:', error);
      const errorMessage = error.response?.data?.detail || 'Registration failed. Please try again.';
      onError(errorMessage);
    }
  };

  return (
    <div className="page">
      <h2 style={{ marginBottom: '20px', color: '#333' }}>Registration</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="Enter your full name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="phone_number">Phone Number</label>
          <input
            type="tel"
            id="phone_number"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            required
            placeholder="10-digit mobile number"
            pattern="[6-9][0-9]{9}"
          />
        </div>

        <div className="form-group">
          <label htmlFor="zone">Zone</label>
          <select
            id="zone"
            name="zone"
            value={formData.zone}
            onChange={handleChange}
            required
          >
            <option value="">Select your work zone</option>
            <option value="bangalore_central">Bangalore Central</option>
            <option value="bangalore_north">Bangalore North</option>
            <option value="bangalore_south">Bangalore South</option>
            <option value="bangalore_east">Bangalore East</option>
            <option value="bangalore_west">Bangalore West</option>
            <option value="mumbai_central">Mumbai Central</option>
            <option value="mumbai_north">Mumbai North</option>
            <option value="mumbai_south">Mumbai South</option>
            <option value="delhi_central">Delhi Central</option>
            <option value="delhi_north">Delhi North</option>
            <option value="delhi_south">Delhi South</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="shift">Shift</label>
          <select
            id="shift"
            name="shift"
            value={formData.shift}
            onChange={handleChange}
            required
          >
            <option value="">Select your preferred shift</option>
            <option value="lunch_peak">Lunch Peak (11 AM - 3 PM)</option>
            <option value="dinner_peak">Dinner Peak (6 PM - 10 PM)</option>
            <option value="full_shift">Full Shift (8 AM - 10 PM)</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="delivery_platform">Delivery Platform</label>
          <select
            id="delivery_platform"
            name="delivery_platform"
            value={formData.delivery_platform}
            onChange={handleChange}
            required
          >
            <option value="">Select your platform</option>
            <option value="swiggy">Swiggy</option>
            <option value="zomato">Zomato</option>
            <option value="zepto">Zepto</option>
            <option value="amazon">Amazon</option>
            <option value="dunzo">Dunzo</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="vehicle_type">Vehicle Type</label>
          <select
            id="vehicle_type"
            name="vehicle_type"
            value={formData.vehicle_type}
            onChange={handleChange}
            required
          >
            <option value="">Select your vehicle</option>
            <option value="bike">Bike</option>
            <option value="scooter">Scooter</option>
            <option value="bicycle">Bicycle</option>
            <option value="car">Car</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="average_daily_earnings">Average Daily Earnings (₹)</label>
          <input
            type="number"
            id="average_daily_earnings"
            name="average_daily_earnings"
            value={formData.average_daily_earnings}
            onChange={handleChange}
            required
            min="200"
            max="2000"
            placeholder="600"
          />
        </div>

        <button type="submit" className="btn">
          Continue
        </button>
      </form>
    </div>
  );
};

export default RegistrationPage;