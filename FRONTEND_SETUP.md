# Frontend Setup & Integration Guide

## Quick Start

### Option 1: Run Both Backend & Frontend Together (Recommended)

**Windows:**
```bash
run-all.bat
```

**macOS/Linux:**
```bash
chmod +x run-all.sh
./run-all.sh
```

This will open two terminal windows:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

---

### Option 2: Run Services Separately

#### Backend (in main project directory)
```bash
python -m uvicorn app.main:app --reload
```

#### Frontend (in frontend folder)
```bash
cd frontend
npm run dev
```

---

## Frontend Structure

```
frontend/
├── src/
│   ├── App.jsx          # Main React component (unified dashboard)
│   └── main.jsx         # Entry point
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite build configuration
├── .env.local           # Environment variables (API URL)
└── node_modules/        # Dependencies (created by npm install)
```

---

## Configuration

### API Endpoint

Edit `frontend/.env.local` to change the backend API URL:

```env
VITE_API_URL=http://localhost:8000
```

**For production deployment**, set this to your production backend URL.

---

## Features

The frontend dashboard includes:

### 📊 **Dashboard**
- Real-time KPIs (active incidents, available teams, response time)
- Weekly incident statistics
- Incident type breakdown (pie chart)
- Weather conditions

### 🚨 **Incidents**
- Create new incidents with category, priority, location
- View all incidents (filter by status)
- Assign teams to incidents
- Close incidents
- View incident details and action logs

### 🗺️ **Live Map**
- Real-time incident markers
- Team location tracking
- High-risk zone overlays
- Navigation integration

### 💬 **Communications**
- WebSocket-based team chat
- Citizen emergency alerts
- Media upload (images/videos)
- Voice note recording

### 📈 **Reports**
- Daily incident summary
- Statistical charts
- Response time trends
- PDF export

### 📦 **Resources**
- Vehicle and equipment tracking
- Fuel level monitoring
- Maintenance scheduling
- Inspection management

### 🌐 **Coordination**
- Inter-agency sharing (Hospital, Police, Fire Dept)
- Weather integration
- Building plan uploads

### 👥 **User Management**
- User creation and role assignment
- Role-based access control (Admin, Dispatcher, Responder, Citizen)

---

## Login Credentials

Use credentials from your backend user database. Default test user:
- **Email:** `admin@eims.gov.lb`
- **Password:** `password` (or as configured in your backend)

---

## Development

### Install Dependencies
```bash
cd frontend
npm install
```

### Run Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000` with hot module reloading.

### Build for Production
```bash
npm run build
```

Output will be in `frontend/dist/`

### Preview Production Build
```bash
npm run preview
```

---

## Backend API Integration

The frontend communicates with the backend at the following endpoints:

- **Authentication:** `POST /api/v1/auth/login/json`
- **Incidents:** `GET/POST /api/v1/incidents/`
- **Media:** `POST /api/v1/media/upload`
- **Reports:** `GET /api/v1/reports/daily`, `GET /api/v1/reports/export/pdf`
- **WebSocket Chat:** `WS /api/v1/ws/chat/{incident_id}`
- **Integrations:** `POST /api/v1/integrations/{agency}/{endpoint}`

See backend API documentation at: `http://localhost:8000/docs`

---

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

For best experience, use a modern browser with ES2020+ support.

---

## Troubleshooting

### Frontend won't connect to backend
1. Verify backend is running on `http://localhost:8000`
2. Check `frontend/.env.local` has correct `VITE_API_URL`
3. Check browser console (F12) for CORS or network errors
4. Backend needs CORS enabled (already configured in `app/main.py`)

### npm install fails
- Delete `node_modules` and `package-lock.json`
- Run `npm cache clean --force`
- Run `npm install` again

### Port already in use
- Backend: Change port in run-all.bat/run-all.sh and `.env.local`
- Frontend: Vite will automatically use next available port (3001, 3002, etc.)

---

## Language Support

The frontend supports bilingual interface:
- **English** (Default)
- **Arabic** (العربية) - Toggle via button in topbar

---

## Performance Notes

- Uses **Vite** for fast development builds
- **Recharts** for data visualization
- **Lucide React** for icons (~50+ icons)
- WebSocket for real-time team chat
- LocalStorage for JWT token persistence

---

## Next Steps

1. ✅ Start both services with `run-all.bat` or `./run-all.sh`
2. Open `http://localhost:3000` in your browser
3. Log in with backend credentials
4. Explore the dashboard and incident management features
5. Check backend API docs at `http://localhost:8000/docs`

