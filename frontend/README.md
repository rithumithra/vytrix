# Vytrix Frontend - React Application

## Overview

This is the React frontend for the Vytrix Insurance Platform. It provides a mobile-first user interface for gig workers to register, calculate premiums, activate policies, and test claim scenarios.

## Features

- **Registration Page**: User registration with zone and shift selection
- **Premium Calculation**: Dynamic premium display with risk factor breakdown
- **Policy Activation**: One-click policy activation
- **Scenario Testing**: Three simulation buttons for testing different scenarios
- **Results Display**: Detailed claim results with scores and decision factors

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running on http://localhost:8000

### Installation

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Start the development server**:
```bash
npm start
```

3. **Open your browser**:
Navigate to http://localhost:3000

## Project Structure

```
frontend/
├── public/
│   └── index.html          # Main HTML template
├── src/
│   ├── components/         # React components
│   │   ├── RegistrationPage.js
│   │   ├── PremiumPage.js
│   │   ├── TriggerPage.js
│   │   ├── ResultPage.js
│   │   └── LoadingPage.js
│   ├── App.js             # Main App component
│   ├── index.js           # React entry point
│   └── index.css          # Global styles
├── package.json           # Dependencies and scripts
└── README.md             # This file
```

## API Integration

The frontend communicates with the FastAPI backend through these endpoints:

- `POST /api/users/register` - User registration
- `POST /api/policies/calculate-premium` - Premium calculation
- `POST /api/policies/activate` - Policy activation
- `POST /api/simulate/rain` - Rain scenario simulation
- `POST /api/simulate/fraud` - Fraud scenario simulation
- `POST /api/simulate/no-activity` - No activity scenario simulation

## User Flow

1. **Registration**: User enters personal details, zone, and shift preferences
2. **Premium Calculation**: System calculates dynamic premium based on risk factors
3. **Policy Activation**: User activates insurance policy
4. **Scenario Testing**: User can test different claim scenarios
5. **Results**: System displays claim processing results with detailed breakdown

## Styling

The application uses vanilla CSS with a mobile-first approach:
- Responsive design optimized for mobile devices
- Clean, modern UI with gradient backgrounds
- Consistent color scheme and typography
- Smooth transitions and hover effects

## Development

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (one-way operation)

### Customization

To customize the UI:
1. Modify styles in `src/index.css`
2. Update component logic in `src/components/`
3. Adjust API endpoints in component files if backend changes

## Production Build

To create a production build:

```bash
npm run build
```

This creates a `build` folder with optimized files ready for deployment.

## Browser Support

The application supports all modern browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### Common Issues

1. **API Connection Failed**:
   - Ensure backend is running on http://localhost:8000
   - Check CORS settings in backend

2. **Registration Fails**:
   - Verify phone number format (10 digits starting with 6-9)
   - Check earnings range (₹200-₹2000)

3. **Simulation Not Working**:
   - Ensure user is registered and policy is activated
   - Check browser console for error messages

### Development Tips

- Use browser developer tools to debug API calls
- Check the Network tab for failed requests
- Console logs are available for debugging
- Backend API documentation available at http://localhost:8000/docs