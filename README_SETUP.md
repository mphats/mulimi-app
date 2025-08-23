# Mlimi App - Setup Guide

## Overview
Mlimi App is a comprehensive agricultural platform built with Django that provides AI-powered pest detection, market prices, weather forecasts, community forums, and product marketplace for farmers in Malawi.

## Features Implemented

### Backend (Django)
- ✅ User authentication system with JWT tokens
- ✅ User roles (Farmer, Agronomist, Trader, Admin)
- ✅ Product marketplace with image uploads
- ✅ Market price tracking
- ✅ Weather data integration
- ✅ AI pest detection service
- ✅ Community forum with posts and replies
- ✅ Newsletter system with multilingual support
- ✅ Rate limiting and permissions
- ✅ Celery integration for async tasks
- ✅ Django admin interface

### Frontend (Django Templates)
- ✅ Responsive Bootstrap-based UI
- ✅ Home page with feature overview
- ✅ User authentication pages (login/register)
- ✅ Product listing and management
- ✅ Market prices display
- ✅ Weather forecast interface
- ✅ Pest detection upload form
- ✅ Community forum interface
- ✅ Newsletter browsing
- ✅ User profile management

### AI Services
- ✅ Pest detection using PlantVillage API
- ✅ Fallback local ML model (scikit-learn)
- ✅ Crop-specific farming advice
- ✅ Market analysis

## Prerequisites
- Python 3.8+
- pip
- Git

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd django-backend-final
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Copy the example environment file and configure it:
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
OPENWEATHER_API_KEY=your-openweather-api-key
PLANTVILLAGE_API_KEY=your-plantvillage-api-key
REDIS_URL=redis://localhost:6379/0
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
django-backend-final/
├── core/                   # Main Django settings
├── api/                    # API endpoints and models
├── users/                  # User management
├── ai/                     # AI services
├── frontend/               # Frontend views and templates
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── requirements.txt        # Python dependencies
├── manage.py              # Django management
└── README.md              # Project documentation
```

## Key Models

- **User & Profile**: Extended user model with roles
- **Product**: Agricultural products for sale
- **MarketPrice**: Real-time market data
- **WeatherData**: Weather forecasts and alerts
- **Newsletter**: Farming tips and updates
- **CommunityPost/Reply**: Forum discussions
- **PestDiagnosis**: AI pest detection results

## API Endpoints

- `/api/v1/auth/` - Authentication endpoints
- `/api/v1/products/` - Product management
- `/api/v1/market-prices/` - Market data
- `/api/v1/weather/` - Weather information
- `/api/v1/pest-detection/` - AI pest detection
- `/api/v1/community/` - Forum posts
- `/api/v1/newsletters/` - Newsletter content

## Frontend Pages

- `/` - Home page
- `/login/` - User login
- `/register/` - User registration
- `/products/` - Product marketplace
- `/market-prices/` - Market price display
- `/weather/` - Weather forecasts
- `/pest-detection/` - AI pest detection
- `/community/` - Community forum
- `/newsletters/` - Farming newsletters
- `/profile/` - User profile management

## Configuration Options

### Database
- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

### Email
- Configure SMTP settings for user verification
- Support for Gmail, SendGrid, etc.

### AI Services
- PlantVillage API for pest detection
- OpenWeather API for weather data
- Fallback local models for offline use

### Redis & Celery
- Redis for caching and task queue
- Celery for background tasks

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### Database Reset
```bash
python manage.py flush
python manage.py migrate
```

## Deployment

### Production Settings
1. Set `DEBUG=False`
2. Configure production database
3. Set up static file serving
4. Configure HTTPS
5. Set up monitoring and logging

### Docker (Optional)
```bash
docker-compose up -d
```

## Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py makemigrations --empty app_name
   python manage.py migrate --fake-initial
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Connection Issues**
   - Check database settings in `.env`
   - Ensure database service is running

4. **Email Not Sending**
   - Verify SMTP settings
   - Check email credentials
   - Test with simple email first

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

## Roadmap

- [ ] Mobile app (React Native/Ionic)
- [ ] Advanced analytics dashboard
- [ ] Machine learning model training
- [ ] Multi-language support expansion
- [ ] Offline-first capabilities
- [ ] Integration with more APIs
- [ ] Advanced reporting features
