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
