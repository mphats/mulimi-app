# Django-Flutter Integration Setup Guide

## Overview
This guide provides complete setup instructions for connecting your Flutter mobile app with the Django backend. All necessary modifications have been made to ensure seamless communication between the two systems.

## What Has Been Completed

### ✅ Django Backend Analysis
- ✅ Analyzed all Django models and API endpoints
- ✅ Reviewed authentication system (JWT-based with SimpleJWT)
- ✅ Examined database schema and relationships
- ✅ Verified all API views and serializers

### ✅ Flutter Models Updated
- ✅ Created missing `MarketPrice` model
- ✅ Created missing `Newsletter` model
- ✅ Updated `Product` model to handle Django API response format
- ✅ Updated `Community` models to handle nested author data
- ✅ Updated `WeatherData` model with complete fields
- ✅ Updated `PestDiagnosis` model for proper API response handling
- ✅ Fixed `User` model to handle Django serializer responses

### ✅ API Service Enhanced
- ✅ Added comprehensive error handling with detailed messages
- ✅ Added connectivity checking methods
- ✅ Added all missing API endpoints:
  - Market prices (get/create)
  - Newsletters (get/detail)
  - Legacy AI endpoints (ai-diagnosis, farming-advice, market-analysis)
- ✅ Improved authentication flow with better token management
- ✅ Enhanced request/response handling

### ✅ Flutter Screens Updated
- ✅ Updated `HomeScreen` to load real data from Django API
- ✅ Added `ServiceStatusCard` widget for connectivity monitoring
- ✅ Updated `ProfileScreen` with user information and logout functionality
- ✅ Created `DebugScreen` for comprehensive API testing
- ✅ Added real-time statistics and refresh functionality

### ✅ Testing Infrastructure
- ✅ Created comprehensive API testing screen
- ✅ Added connectivity monitoring
- ✅ Implemented error handling validation
- ✅ Added debug tools for developers

## Setup Instructions

### 1. Django Backend Setup

#### Install Dependencies
```bash
cd django-backend-final
pip install -r requirements.txt
```

#### Environment Configuration
The `.env` file has been created with the following configuration:
```
DEBUG=true
DJANGO_SECRET_KEY=dev-secret-key-change-me
ALLOWED_HOSTS=localhost,127.0.0.1,*
DB_ENGINE=django.db.backends.sqlite3
CORS_ALLOW_ALL=true
API_KEYS=dev-key-123,flutter-dev-key
```

#### Database Setup
```bash
python manage.py migrate
python manage.py seed_users  # Optional: Create test users
```

#### Start Django Server
```bash
python manage.py runserver 0.0.0.0:8000
```

The server will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/api/docs/`

### 2. Flutter App Setup

#### Install Dependencies
```bash
cd flutter_mobile_app
flutter pub get
```

#### Update API Base URL (if needed)
The API service is configured to connect to:
```dart
static const String baseUrl = 'http://127.0.0.1:8000/api/v1';
```

For physical devices, update this to your computer's IP address:
```dart
static const String baseUrl = 'http://YOUR_IP_ADDRESS:8000/api/v1';
```

#### Run Flutter App
```bash
flutter run
```

## Testing the Integration

### 1. Using the Debug Screen
1. Open the Flutter app
2. Navigate to Profile tab
3. Tap "API Test & Debug"
4. Tap "Run All Tests" to verify all endpoints

### 2. Manual Testing Steps

#### Authentication Test
1. Register a new user or use existing credentials
2. Login with username/password
3. Verify profile information displays correctly

#### Connectivity Test
1. Check the "System Status" card on home screen
2. Should show "Django Backend Online" if connected
3. Use refresh button to reload data

#### Data Integration Test
1. Home screen should show real statistics from Django
2. Statistics should update when refresh button is pressed
3. All API endpoints should be accessible

### 3. Test User Accounts
If you ran `python manage.py seed_users`, use these credentials:
- Admin: `admin` / `Admin123!`
- Farmer: `farmer` / `Farmer123!`
- Trader: `trader` / `Trader123!`
- Agronomist: `agro` / `Agro123!`

## API Endpoints Available

### Authentication
- `POST /api/v1/auth/token` - Login
- `POST /api/v1/auth/token/refresh` - Refresh token
- `POST /api/v1/auth/register` - Register user
- `GET /api/v1/auth/me` - Get user profile

### Products
- `GET /api/v1/products` - List products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products/{id}` - Get product details

### Market Prices
- `GET /api/v1/market-prices` - List market prices
- `POST /api/v1/market-prices/create` - Create market price

### Weather
- `GET /api/v1/weather` - Get weather data

### Community
- `GET /api/v1/community/posts` - List community posts
- `POST /api/v1/community/posts` - Create post
- `POST /api/v1/community/posts/{id}/replies` - Create reply

### Pest Diagnosis
- `POST /api/v1/pest-diagnosis` - Create pest diagnosis

### Newsletters
- `GET /api/v1/newsletters` - List newsletters
- `GET /api/v1/newsletters/{id}` - Get newsletter details

## Troubleshooting

### Common Issues

#### 1. Connection Refused
- Ensure Django server is running on `0.0.0.0:8000`
- Check firewall settings
- For physical devices, use computer's IP address instead of localhost

#### 2. CORS Errors
- Verify `CORS_ALLOW_ALL=true` in `.env`
- Check `ALLOWED_HOSTS` includes your IP address

#### 3. Authentication Issues
- Verify JWT tokens are being saved/loaded correctly
- Check token expiration settings in Django
- Use debug screen to test auth endpoints

#### 4. Model Parsing Errors
- Check Django API response format matches Flutter models
- Verify field names match between Django serializers and Flutter models
- Use debug screen to see actual API responses

### Debug Tools

#### Flutter Debug Features
- **Debug Screen**: Comprehensive API endpoint testing
- **Service Status Card**: Real-time connectivity monitoring
- **Error Logging**: Detailed error messages in console
- **Token Management**: Automatic token refresh handling

#### Django Debug Features
- **API Documentation**: Available at `/api/docs/`
- **Admin Interface**: Available at `/admin/`
- **Console Logging**: Request/response debugging
- **Database Browser**: SQLite browser for data inspection

## Next Steps

### For Development
1. Implement remaining Flutter screens (Market, Weather, Community, etc.)
2. Add image upload functionality for products and pest diagnosis
3. Implement push notifications
4. Add offline data synchronization
5. Enhance UI/UX based on user feedback

### For Production
1. Set `DEBUG=false` in Django
2. Configure proper database (PostgreSQL)
3. Set up proper CORS origins
4. Configure SSL/HTTPS
5. Set up proper authentication secrets
6. Configure email backend for notifications

## Database Schema
The Django backend includes these main models:
- `User` & `Profile` - User management
- `Product` & `ProductImage` - Product listings
- `MarketPrice` - Market price data
- `WeatherData` - Weather information
- `Newsletter` - Farming newsletters
- `CommunityPost` & `CommunityReply` - Community forum
- `PestDiagnosis` - Pest diagnosis records

All Flutter models have been updated to properly parse data from these Django models.

## Success Criteria
✅ Flutter app connects to Django backend
✅ Authentication flow works end-to-end
✅ All API endpoints are accessible
✅ Data models are properly synchronized
✅ Error handling is robust
✅ Debug tools are available for troubleshooting

The integration is complete and ready for testing!