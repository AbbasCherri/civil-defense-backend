# Civil Defense Emergency Management System – Backend

This repository contains the backend API and business logic for the Civil Defense Emergency Management System. It is built with Django and provides services for incident management, resource tracking, user authentication, notifications, reporting, and integration with external agencies.

## Overview

The backend serves as the central hub for all data and logic. It exposes a RESTful API consumed by the **web dispatch console** and the **Android mobile app**. Key responsibilities include:

- User authentication and role‑based access control (JWT)
- Incident creation, assignment, and lifecycle management
- Real‑time resource (vehicles, equipment, personnel) tracking
- Push notifications via Firebase Cloud Messaging (FCM)
- PDF report generation (daily summaries, statistics)
- Geospatial queries (nearby teams, high‑risk zones)
- Integration mocks for hospitals, police, and fire departments

## Prerequisites

- Python 3.10+
- MySQL 8.0+
- (Optional) Firebase project for FCM
- Git

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbbasCherri/civil-defense-backend.git
   cd civil-defense-backend
   ```
2. **Set up a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
3. **Install dependencies**
```bash
pip install -r requirements/dev.txt
```
4. **Configure environment variables**
   - copy `.env.example` to `.env`
   - edit `.env` with your database credentials, secret key, and FCM settings
5. **Run database migrations**
```bash
python manage.py migrate
```
6. **Start the development server**
```bash
python manage.py runserver
```
The API will be available at `http://localhost:8000`.