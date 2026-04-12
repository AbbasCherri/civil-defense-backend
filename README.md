# Civil Defense Emergency Management System - Backend API

A production-ready FastAPI backend for a comprehensive Civil Defense Emergency Management System with real-time incident management, team dispatch, live location tracking, and integrated external service communications.

## Features

- **Role-Based Access Control (RBAC)**
  - Citizen: Report incidents
  - Dispatcher: Manage incidents, assign teams, view live map
  - Responder: Receive alerts, update location, participate in chat
  - Admin: System administration and user management
  - External: API integrations with external services

- **Real-Time Communication**
  - WebSocket support for live map updates
  - Real-time chat messaging for incident teams
  - Push alerts to responders

- **Incident Management**
  - Create, read, update incident information
  - Track incident status (Waiting, Active, Closed)
  - Categorize incidents (Fire, Medical, Traffic, etc.)
  - Prioritize incidents (Low, Medium, High, Critical)

- **Team Management**
  - Create and manage response teams
  - Assign teams to incidents
  - Track team status and vehicle assignments

- **Media Handling**
  - File upload support (images, videos, voice notes, documents)
  - Secure local file storage

- **Reporting**
  - Daily incident statistics
  - PDF report generation with ReportLab
  - Date range filtering

- **External Integrations**
  - Mock APIs for Police, Fire, and Hospital systems
  - Request/response handling for external services

- **Audit Logging**
  - Track all critical system actions
  - Complete audit trail for compliance

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with async SQLAlchemy ORM
- **Migrations**: Alembic
- **Authentication**: JWT with bcrypt password hashing
- **Real-Time**: WebSockets
- **PDF Generation**: ReportLab
- **Data Validation**: Pydantic v2
- **Server**: Uvicorn

## Architecture

```
app/
├── api/
│   └── v1/
│       └── routers/
│           ├── auth.py              # Authentication endpoints
│           ├── incidents.py          # Incident CRUD
│           ├── media.py              # File upload
│           ├── resources.py           # Resource management
│           ├── reports.py            # Reports and PDF generation
│           ├── websocket.py          # Real-time communication
│           └── integrations.py       # External service integrations
├── core/
│   ├── config.py                    # Configuration settings
│   ├── database.py                  # Database setup
│   └── security.py                  # Authentication & security
├── models/
│   └── models.py                    # SQLAlchemy ORM models
├── repositories/                    # Data access layer
├── services/                        # Business logic layer
├── schemas/                         # Pydantic schemas
└── main.py                          # FastAPI application
```

## Installation & Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip or conda

### Step 1: Clone and Navigate to Project

```bash
cd "Website Backend Project"
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup PostgreSQL Database

1. **Open pgAdmin 4**
   - Navigate to http://localhost:5050
   - Login with your pgAdmin credentials

2. **Create Database**
   - Right-click "Databases" → "Create" → "Database"
   - Name: `civil_defense_db`
   - Owner: `postgres`
   - Click "Save"

3. **Verify Connection**
   - Expand "Databases" to see `civil_defense_db`
   - Properties should show Port: 5432, Username: postgres

### Step 5: Configure Environment Variables

```bash
# Copy environment example file
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/civil_defense_db
SECRET_KEY=change-this-to-a-random-secret-key
JWT_SECRET_KEY=change-this-to-a-random-jwt-secret
DEBUG=False
```

### Step 6: Initialize Database with Alembic

```bash
# Initialize migration environment (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Step 7: Start the Development Server

**Windows (PowerShell):**
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**macOS/Linux:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: **http://localhost:8000**

## API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints Overview

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Incidents
- `POST /api/v1/incidents/` - Create incident
- `GET /api/v1/incidents/` - List incidents
- `GET /api/v1/incidents/{incident_id}` - Get incident details
- `PATCH /api/v1/incidents/{incident_id}/status` - Update incident status
- `POST /api/v1/incidents/{incident_id}/assign-team` - Assign team to incident
- `GET /api/v1/incidents/date-range` - Get incidents by date range

### Media
- `POST /api/v1/media/upload` - Upload media file
- `GET /api/v1/media/incident/{incident_id}` - Get incident media
- `DELETE /api/v1/media/{media_id}` - Delete media file

### Resources
- `POST /api/v1/resources/` - Create resource
- `GET /api/v1/resources/` - List resources
- `GET /api/v1/resources/{resource_id}` - Get resource details
- `PATCH /api/v1/resources/{resource_id}` - Update resource
- `PATCH /api/v1/resources/{resource_id}/status` - Update resource status
- `PATCH /api/v1/resources/{resource_id}/fuel` - Update fuel usage
- `PATCH /api/v1/resources/{resource_id}/inspect` - Mark inspection

### Reports
- `GET /api/v1/reports/daily` - Get daily statistics (JSON)
- `GET /api/v1/reports/export/pdf` - Export PDF report

### WebSockets
- `WS /api/v1/ws/live-map/{incident_id}` - Live map updates
- `WS /api/v1/ws/chat/{incident_id}` - Real-time chat

### Integrations
- `POST /api/v1/integrations/hospital/admission` - Send hospital admission request
- `POST /api/v1/integrations/police/incident-report` - Send police incident report
- `POST /api/v1/integrations/fire-department/request` - Send fire department request
- `GET /api/v1/integrations/hospital/status/{case_id}` - Get hospital status
- `GET /api/v1/integrations/police/status/{case_number}` - Get police status
- `GET /api/v1/integrations/fire-department/status/{request_id}` - Get fire status

## Testing the API

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Dispatcher",
    "email": "dispatcher@example.com",
    "password": "securepassword123",
    "role": "Dispatcher",
    "contact_info": "+1234567890"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "dispatcher@example.com",
    "password": "securepassword123"
  }'
```

Response will contain your JWT token:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create an Incident

```bash
curl -X POST http://localhost:8000/api/v1/incidents/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "category": "Fire",
    "priority": "High",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "description": "Building fire on Main Street"
  }'
```

### 4. Upload Media

```bash
curl -X POST http://localhost:8000/api/v1/media/upload \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "incident_id=1" \
  -F "file_type=image" \
  -F "file=@/path/to/image.jpg"
```

### 5. Get PDF Report

```bash
curl -X GET "http://localhost:8000/api/v1/reports/export/pdf?start_date=2024-01-01&end_date=2024-12-31" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -o report.pdf
```

## Database Schema

### Users Table
- id (PK)
- name
- email (unique)
- password_hash
- role (enum: Citizen, Dispatcher, Responder, Admin, External)
- contact_info
- created_at

### Incidents Table
- id (PK)
- citizen_id (FK)
- category (enum: Fire, Medical, Traffic, Accident, Flood, Other)
- priority (enum: Low, Medium, High, Critical)
- status (enum: Waiting, Active, Closed)
- latitude
- longitude
- description
- created_at
- closed_at

### Teams Table
- id (PK)
- vehicle_id (FK)
- status (enum: Available, Deployed)
- created_at

### Resources Table
- id (PK)
- name
- type (enum: Vehicle, Equipment)
- status (enum: Available, Unavailable, Maintenance)
- fuel_usage
- last_inspection
- created_at

### Additional Tables
- Media (incident_id, file_path, file_type)
- TeamMembers (team_id, user_id)
- TeamAssignments (team_id, incident_id)
- Messages (sender_id, incident_id, content)
- AuditLogs (user_id, action, target_entity, timestamp)

## Workflow Example

1. **Incident Reporting** (Citizen)
   - POST `/incidents/` → Creates incident with status "Waiting"
   - WebSocket alert sent to all Dispatchers

2. **Dispatch** (Dispatcher)
   - GET `/incidents/available-teams` → Gets list of available teams
   - POST `/incidents/{id}/assign-team` → Assigns team, status → "Active"
   - Audit log created

3. **Live Updates** (Responder)
   - WS `live-map/{incident_id}` → Sends GPS coordinates
   - Coordinates broadcast to all connected users
   - WS `chat/{incident_id}` → Chat with team members

4. **Closure** (Dispatcher/Responder)
   - PATCH `/incidents/{id}/status` → status = "Closed", closed_at = now
   - Team status → "Available"
   - Audit log created

## Security Considerations

- All passwords hashed with bcrypt
- JWT tokens with 30-minute expiration
- CORS configured for specific origins
- Role-based access control on all endpoints
- Database credentials in environment variables
- Audit logging for all critical actions

## Environment Setup for Production

Before deploying to production:

1. Change all SECRET_KEY and JWT_SECRET_KEY values
2. Set DEBUG=False
3. Configure proper CORS_ORIGINS
4. Use stronger database passwords
5. Enable HTTPS
6. Set up proper logging
7. Consider using a process manager (Gunicorn, Supervisor)

## Troubleshooting

### Database Connection Error
```
Error: could not translate host name "localhost" to address
```
**Solution**: Verify PostgreSQL is running and credentials in `.env` are correct

### Alembic Migration Issues
```
Error: Table already exists
```
**Solution**: Check if migrations were already applied, or drop and recreate database

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Change port with `--port 8001` or kill process using port 8000

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

This project is provided as-is for emergency management purposes.

## Support

For issues or questions, refer to the API documentation at `/docs` endpoint while the server is running.
