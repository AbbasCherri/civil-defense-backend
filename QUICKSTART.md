# Quick Start Guide - Civil Defense Backend API

## For Windows Users (Recommended)

### Quick Setup (5 minutes)

1. **Navigate to Project Directory**
   ```
   cd "Website Backend Project"
   ```

2. **Run the Setup Script**
   Double-click `run.bat` or run in PowerShell:
   ```powershell
   .\run.bat
   ```

3. **Wait for Migrations** (first time only takes ~30 seconds)

4. **Access API**
   - Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Manual Setup (if run.bat has issues)

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy env file
Copy-Item .env.example .env

# Update .env with database credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Database Setup (First Time)

### Option 1: Using pgAdmin (GUI)
1. Open pgAdmin 4 (http://localhost:5050)
2. Right-click "Databases" → Create → Database
3. Name: `civil_defense_db`
4. Owner: `postgres`
5. Click Save

### Option 2: Using Command Line
```powershell
# Connect to PostgreSQL
psql -U postgres

# In PostgreSQL prompt
CREATE DATABASE civil_defense_db;
\q
```

## Testing the API

### 1. Open Swagger UI
Visit: http://localhost:8000/docs

### 2. Register a User
- Click "Try it out" on `/api/v1/auth/register`
- Enter:
  ```json
  {
    "name": "John Dispatcher",
    "email": "dispatcher@test.com",
    "password": "test123456",
    "role": "Dispatcher",
    "contact_info": "+1234567890"
  }
  ```
- Click "Execute"

### 3. Login
- Use `/api/v1/auth/login` endpoint
- Enter email and password from registration
- Copy the `access_token` value

### 4. Create Incident
- Click "/api/v1/incidents/" endpoint
- Click "Authorize" and paste token (format: `Bearer <token>`)
- Enter:
  ```json
  {
    "category": "Fire",
    "priority": "High",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "description": "Test incident"
  }
  ```
- Click "Execute"

## Project Structure Overview

```
Website Backend Project/
├── app/                          # Main application
│   ├── main.py                  # FastAPI app entry point
│   ├── api/v1/routers/          # API endpoints
│   │   ├── auth.py              # Authentication
│   │   ├── incidents.py         # Incident management
│   │   ├── media.py             # File uploads
│   │   ├── resources.py         # Vehicle/Equipment
│   │   ├── reports.py           # Reports & PDF
│   │   ├── websocket.py         # Real-time communication
│   │   └── integrations.py      # External services
│   ├── models/                  # Database models
│   ├── schemas/                 # Pydantic validators
│   ├── services/                # Business logic
│   ├── repositories/            # Data access
│   └── core/                    # Config & security
├── alembic/                     # Database migrations
├── uploads/                     # File storage
├── requirements.txt             # Dependencies
├── .env.example                 # Environment template
├── run.bat                      # Windows run script
├── run.sh                       # Linux/Mac run script
└── README.md                    # Full documentation
```

## Available Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login (get token)

### Incidents
- `POST /api/v1/incidents/` - Create
- `GET /api/v1/incidents/` - List
- `GET /api/v1/incidents/{id}` - Details
- `PATCH /api/v1/incidents/{id}/status` - Update status
- `POST /api/v1/incidents/{id}/assign-team` - Assign team

### Media
- `POST /api/v1/media/upload` - Upload file
- `GET /api/v1/media/incident/{incident_id}` - List files
- `DELETE /api/v1/media/{media_id}` - Delete file

### Resources
- `POST /api/v1/resources/` - Create resource
- `GET /api/v1/resources/` - List resources
- `PATCH /api/v1/resources/{id}` - Update resource

### Reports
- `GET /api/v1/reports/daily` - Daily stats (JSON)
- `GET /api/v1/reports/export/pdf` - PDF report

### WebSockets
- `WS /api/v1/ws/live-map/{incident_id}` - Live location tracking
- `WS /api/v1/ws/chat/{incident_id}` - Team chat

### Integrations
- `POST /api/v1/integrations/hospital/admission`
- `POST /api/v1/integrations/police/incident-report`
- `POST /api/v1/integrations/fire-department/request`

## Troubleshooting

### "Port 8000 already in use"
Change port in command:
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### "Database connection refused"
- Check PostgreSQL is running
- Verify database name in .env
- Check credentials are correct

### "ModuleNotFoundError"
Ensure virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
```

### "No module named..."
Install requirements:
```powershell
pip install -r requirements.txt
```

## Environment Configuration

Edit `.env` file with your settings:

```env
# Database - Update with your credentials
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/civil_defense_db

# Security - Change these in production!
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# CORS - Allow frontend domains
CORS_ORIGINS=["*"]

# Development
DEBUG=True
```

## User Roles

- **Citizen**: Report incidents
- **Dispatcher**: Manage incidents & teams
- **Responder**: Receive alerts & update location
- **Admin**: System administration
- **External**: API integrations

When registering, use role value: `Citizen`, `Dispatcher`, `Responder`, `Admin`, or `External`

## Next Steps

1. ✅ Start the server with `run.bat`
2. ✅ Test endpoints in Swagger UI (`/docs`)
3. ✅ Register test users for each role
4. ✅ Create test incidents
5. ✅ Test file uploads
6. ✅ Generate PDF reports

## Production Deployment

Before deploying:

1. Change `SECRET_KEY` and `JWT_SECRET_KEY`
2. Set `DEBUG=False`
3. Configure `CORS_ORIGINS` properly
4. Use strong database password
5. Set up HTTPS/SSL
6. Use production database server
7. Set up logging and monitoring

See `README.md` for complete documentation.
