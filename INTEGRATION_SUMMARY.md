# Frontend Integration - Setup Complete ✅

## Overview

Your React frontend has been successfully integrated with your backend. The frontend is a comprehensive emergency management dashboard with features for dispatchers, administrators, and decision makers.

---

## What Was Set Up

### 1. **Frontend Repository**
- ✅ Cloned from: `https://github.com/AbbasCherri/civil-defense-web`
- ✅ Location: `frontend/` subdirectory
- ✅ Framework: React 18 with Vite (fast build tool)

### 2. **Project Structure Created**
```
frontend/
├── src/
│   ├── App.jsx          ← Main React dashboard component
│   ├── main.jsx         ← Entry point
├── index.html           ← HTML template
├── package.json         ← Dependencies configuration
├── vite.config.js       ← Build configuration
├── .env.local           ← API endpoint (http://localhost:8000)
├── dist/                ← Production build output
└── node_modules/        ← Dependencies installed
```

### 3. **Dependencies Installed**
- **React 18.2.0** - UI library
- **Recharts 2.10.0** - Data visualization (charts, graphs)
- **Lucide React 0.294.0** - Icon library (~50+ icons)
- **Vite 5.0.0** - Fast build tool and dev server

### 4. **Startup Scripts Created**
Two convenient startup scripts to run both backend and frontend together:

**Windows:**
```bash
run-all.bat
```

**macOS/Linux:**
```bash
run-all.sh
```

### 5. **API Configuration**
Frontend configured to connect to backend at: `http://localhost:8000`
Edit: `frontend/.env.local` to change API endpoint

---

## Quick Start Guide

### Start Everything in One Command

**Windows (PowerShell/CMD):**
```bash
.\run-all.bat
```

**macOS/Linux (Terminal):**
```bash
chmod +x run-all.sh
./run-all.sh
```

This opens 2 terminal windows:
- **Backend:**  http://localhost:8000
- **Frontend:** http://localhost:3000

### Or Start Services Separately

**Terminal 1 - Backend:**
```bash
python -m uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

---

## Dashboard Features

The frontend includes a complete emergency management system:

### 📊 **Dashboard**
- Real-time KPI display (active incidents, response times)
- Weekly incident trends
- Incident breakdown by type
- Live weather widget

### 🚨 **Incidents**
- Create new incidents with priority & category
- Filter by status (active, pending, closed)
- Assign teams to incidents
- View incident timeline/audit logs

### 🗺️ **Live Map**
- Real-time incident visualization
- Team location tracking
- High-risk zone overlays
- GPS navigation integration

### 💬 **Communications**
- WebSocket-based team chat
- Citizen emergency alerts
- Image/video upload
- Voice note recording

### 📈 **Reports**
- Daily incident summaries
- Statistical analysis
- Response time trends
- PDF export functionality

### 📦 **Resources**
- Vehicle/equipment tracking
- Fuel level monitoring
- Maintenance scheduling

### 👥 **User Management**
- Create users with roles
- Role-based access control
- Admin, Dispatcher, Responder, Citizen roles

### 🌐 **Coordination**
- Inter-agency sharing (Hospital, Police, Fire Dept)
- Building plan uploads

---

## Login Information

Use your backend database credentials:
- **Email:** admin@eims.gov.lb (or any registered user)
- **Password:** As configured in your backend

---

## API Connection

The frontend communicates with backend at:
- **Login:** `POST /api/v1/auth/login/json`
- **Incidents:** `GET/POST /api/v1/incidents/`
- **WebSocket:** `WS /api/v1/ws/chat/{incident_id}`
- **Media Upload:** `POST /api/v1/media/upload`
- **Reports:** `GET /api/v1/reports/daily`, `GET /api/v1/reports/export/pdf`
- **Integrations:** `POST /api/v1/integrations/{agency}/{endpoint}`

Backend API docs: `http://localhost:8000/docs` (Swagger UI)

---

## Next Steps

1. **Start Everything:**
   ```bash
   .\run-all.bat    # Windows
   ./run-all.sh     # macOS/Linux
   ```

2. **Open Frontend:**
   ```
   http://localhost:3000
   ```

3. **Log In:**
   - Use credentials from your backend database
   - Dispatcher/Admin accounts have full access

4. **Explore Features:**
   - Create test incidents
   - View live map
   - Check dashboard statistics
   - Test team assignment

5. **Verify API Connection:**
   - Open backend docs: `http://localhost:8000/docs`
   - Check CORS is configured (already enabled in `app/main.py`)

---

## Configuration Files

### 1. `frontend/.env.local`
```env
VITE_API_URL=http://localhost:8000
```
Change to your production backend URL when deploying.

### 2. `frontend/vite.config.js`
Configured for:
- Dev server on port 3000
- Auto-reload on file changes
- Production build output to `dist/`

### 3. `frontend/package.json`
Scripts available:
- `npm run dev` - Start dev server
- `npm run build` - Create production build
- `npm run preview` - Preview production build

---

## Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
```

### Output
- `frontend/dist/` contains production-ready files
- Can be deployed to any static hosting:
  - AWS S3
  - Netlify
  - Vercel
  - GitHub Pages
  - Docker container
  - Your own web server

### Update API Endpoint
Before deploying, update `frontend/.env.local`:
```env
VITE_API_URL=https://your-production-backend.com
```

---

## Troubleshooting

### Frontend won't connect to backend
```
1. Check backend is running: http://localhost:8000/docs
2. Check .env.local has correct VITE_API_URL
3. Check browser console (F12) for errors
4. Check CORS - already enabled in backend
```

### npm install fails
```bash
rm -r node_modules package-lock.json  # macOS/Linux
rmdir /s node_modules                 # Windows
npm cache clean --force
npm install
```

### Port already in use
- Backend: Edit run-all.bat/sh and .env.local (change 8000)
- Frontend: Vite will auto-use next port (3001, 3002, etc)

### Build warnings about chunk size
- Normal for single-component architecture
- Won't affect functionality
- Consider code-splitting if needed later

---

## Bilingual Support

Frontend supports:
- **English** (default)
- **Arabic** - Toggle via language button in top-right

All labels, buttons, and navigation automatically adjust.

---

## File Structure Reference

```
Website Backend Project/
├── app/                          ← Backend code
│   ├── main.py                   ← FastAPI app
│   ├── core/
│   │   ├── config.py             ← CORS configured here
│   │   └── database.py
│   └── api/
│       └── v1/
│           └── routers/
├── frontend/                     ← React frontend (NEW)
│   ├── src/
│   │   ├── App.jsx               ← Main dashboard
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── .env.local                ← API config
├── run-all.bat                   ← Run both (NEW)
├── run-all.sh                    ← Run both (NEW)
├── FRONTEND_SETUP.md             ← Detailed guide (NEW)
└── INTEGRATION_SUMMARY.md        ← This file (NEW)
```

---

## Key Technologies

- **React 18** - UI framework
- **Vite** - Build tool (10x faster than Create React App)
- **Recharts** - Interactive charts
- **Lucide Icons** - Modern icon library
- **WebSocket** - Real-time team chat
- **JWT** - Secure authentication

---

## Support & Documentation

- **Backend Docs:** `http://localhost:8000/docs` (Swagger)
- **Frontend Source:** `frontend/src/App.jsx` (~2500 lines comprehensive component)
- **Setup Guide:** `FRONTEND_SETUP.md`
- **GitHub Backend:** Your local repository

---

## What's Next

### Immediate
1. ✅ Start services with `run-all.bat`
2. ✅ Test login with backend credentials
3. ✅ Create test incidents
4. ✅ Verify map and dashboard work

### Short-term
1. Deploy to staging environment
2. Load test with real data
3. Configure production API URL
4. Set up SSL/TLS certificates

### Long-term
1. Implement push notifications
2. Add mobile app companion
3. Enhance analytics
4. Multi-language support improvements

---

**Status: ✅ Complete - Ready to Use!**

Your frontend is fully integrated with your backend and ready for development and testing.
