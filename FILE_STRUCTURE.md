# Backend File Structure – Expected Contents

This document describes the intended purpose of each directory and the types of files that will reside there as the project develops. Use it as a guide when adding new features or exploring the codebase.

## Root Directory

| File/Dir          | Expected Contents |
|-------------------|-------------------|
| `README.md`       | Project overview, setup instructions, quick start. |
| `FILE_STRUCTURE.md` | This file. |
| `.env.example`    | Template for environment variables (never commit real secrets). |
| `.gitignore`      | List of files/folders ignored by Git (e.g., `venv/`, `__pycache__/`, `.env`). |
| `manage.py`       | Django’s command-line utility for administrative tasks. |
| `requirements/`   | Dependency files split by environment (see below). |
| `config/`         | Django project configuration (settings, URLs, WSGI/ASGI). |
| `apps/`           | All custom Django applications (each a self-contained module). |
| `static/`         | Collected static files (CSS, JS, images) – used in production. |
| `media/`          | User-uploaded files (photos, videos, voice notes). |
| `templates/`      | Project-wide HTML templates (e.g., email templates, base layouts). |
| `scripts/`        | Standalone utility scripts (data seeding, backups, one-off tasks). |
| `tests/`          | Integration and end-to-end tests that span multiple apps. |
| `docs/`           | Additional documentation (API contracts, ADRs, meeting notes). |

## `requirements/` – Python Dependencies

| File          | Purpose |
|---------------|---------|
| `base.txt`    | Dependencies common to all environments (Django, MySQL client, etc.). |
| `dev.txt`     | Development-only packages (debug toolbar, pytest, ipython). Includes `-r base.txt`. |
| `prod.txt`    | Production-only packages (gunicorn, uvicorn). Includes `-r base.txt`. |


## `config/` – Project Configuration

| File/Dir          | Expected Contents |
|-------------------|-------------------|
| `settings/`       | Environment‑specific settings modules. |
| │─ `base.py`      | Shared settings (database, installed apps, middleware, templates, etc.). |
| │─ `dev.py`       | Development overrides (debug=True, local DB, etc.). Imports from `base.py`. |
| │─ `prod.py`      | Production overrides (debug=False, security settings, production DB). Imports from `base.py`. |
| `urls/`           | Project‑level URL routing (can split into multiple files if needed). |
| │─ `base.py`      | Main URL patterns including `admin/` and app inclusions. |
| `asgi.py`         | ASGI entry point for async servers. |
| `wsgi.py`         | WSGI entry point for traditional WSGI servers. |


## `apps/` – Custom Django Applications

Each app follows a similar internal structure. Below is the typical layout for an app like `incidents`:

```
apps/incidents/
├── migrations/          # Database migrations (auto‑generated)
├── templates/           # App‑specific HTML templates (if any)
├── __init__.py
├── admin.py             # Django admin configuration
├── apps.py              # App configuration
├── models.py            # Database models
├── serializers.py       # DRF serializers (convert data to/from JSON)
├── views.py             # Request handlers (API endpoints)
├── urls.py              # App‑specific URL routing
├── permissions.py       # Custom permission classes (if needed)
├── signals.py           # Django signals (e.g., post‑save triggers)
├── utils.py             # Helper functions specific to this app
├── tests/               # Unit tests for this app
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── ...
└── ...
```

### What each app will contain:

#### `accounts/`
- **Purpose:** User authentication, profiles, role‑based access control (RBAC), JWT handling.
- **Key files:** `models.py` (User, Profile), `serializers.py` (registration, login), `views.py` (signup, login, token refresh), `permissions.py` (role checks), `utils.py` (JWT helpers).

#### `incidents/`
- **Purpose:** Core incident management – creation, assignment, status updates, evidence (photos, videos, voice notes).
- **Key files:** `models.py` (Incident, IncidentMedia, Assignment), `serializers.py` (incident creation, evidence upload), `views.py` (CRUD endpoints), `utils.py` (geospatial helpers), `signals.py` (trigger notifications on assignment).

#### `resources/`
- **Purpose:** Manage vehicles, equipment, personnel, and their availability.
- **Key files:** `models.py` (Vehicle, Tool, Employee), `serializers.py`, `views.py` (status updates, inventory), `utils.py` (availability checks).

#### `notifications/`
- **Purpose:** Push notifications (FCM), alerts to responders and citizens.
- **Key files:** `models.py` (Notification, Device), `serializers.py`, `views.py` (register device), `utils.py` (FCM sender), `signals.py` (send notification on certain events).

#### `reporting/`
- **Purpose:** Generate daily reports, statistical summaries, PDF exports, and provide dashboard data.
- **Key files:** `models.py` (Report, maybe none), `serializers.py`, `views.py` (report endpoints), `utils.py` (PDF generation with ReportLab), `services.py` (query logic for KPIs).

#### `integration/`
- **Purpose:** Simulate or connect with external agencies (hospitals, police, fire departments) and fetch weather data.
- **Key files:** `models.py` (maybe none), `serializers.py`, `views.py` (mock endpoints), `utils.py` (external API clients), `services.py` (data aggregation).

#### `common/`
- **Purpose:** Reusable utilities shared across apps.
- **Key files:** `models.py` (abstract base classes, timestamped model), `utils.py` (generic helpers, validators), `decorators.py` (custom decorators like `@log_action`), `exceptions.py` (custom exception classes), `pagination.py` (custom pagination classes), `middleware.py` (custom middleware if any).


## `static/` and `media/`

- **`static/`** – After running `collectstatic`, this folder will contain all static files from Django apps and any global static assets. It is served in production.
- **`media/`** – User‑uploaded files are stored here during development. In production, you might replace this with cloud storage (e.g., AWS S3). Subdirectories may be created automatically by the application (e.g., `media/incident_photos/`, `media/voice_notes/`).

## `templates/`

Contains HTML templates that are not tied to a specific app. Examples:
- `emails/` – Email templates (e.g., alert notifications, password reset).
- `base.html` – Base template that other templates extend (if using server‑side rendering, though this API may not need it).


## `scripts/`

Standalone Python scripts for utility tasks. They are not part of the Django application and are run manually. Examples:
- `seed_data.py` – Populate the database with fake users, incidents, etc.
- `backup_db.py` – Automated database backup.
- `migrate_data.py` – One‑off data migrations that are not handled by Django migrations.

## `tests/`

Houses tests that span multiple apps. For app‑specific tests, they belong inside each app's `tests/` directory. The `tests/` folder here can contain:
- `integration/` – Tests that verify interactions between apps.
- `performance/` – Load tests to ensure response time requirements.
- `conftest.py` – Pytest fixtures shared across tests.


## `docs/`

Long‑lived documentation:
- `API.md` – Detailed API documentation (if not using auto‑generated Swagger).
- `ARCHITECTURE.md` – High‑level architectural decisions.
- `CONTRACTS/` – OpenAPI specification files (JSON/YAML).
- `MEETING_NOTES/` – Notes from team meetings (optional).


## Notes

- This structure follows Django best practices and is designed to be intuitive for new developers.
- As the project grows, new apps or directories may be added. Always keep this document updated so it remains a reliable reference.
- If you are unsure where a new file should go, consult this guide or ask the team.
