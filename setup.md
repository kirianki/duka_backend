# ShopOS Backend Setup Guide

This guide will help you get the ShopOS backend (Django REST Framework) up and running.

## Prerequisites
- Docker & Docker Compose
- Python 3.12+ (for local development/testing)

## Quick Start (Docker)

1. **Configure Environment Variables**
   Create a `.env` file in the `backend/` directory:
   ```bash
   # .env example
   POSTGRES_DB=shopos
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   SECRET_KEY=your-secret-key
   DEBUG=True
   ```

2. **Build and Run**
   ```bash
   docker compose up --build
   ```
   The backend will:
   - Wait for the database.
   - Automatically run migrations.
   - Collect static files.
   - Start the development server at `http://localhost:8000`.

3. **Access API Documentation**
   Visit `http://localhost:8000/api/schema/swagger-ui/` for the interactive Swagger UI.

## Local Development (Non-Docker)

1. **Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Database Fallback**
   If no PostgreSQL is detected (or `/.dockerenv` is missing), the app will fallback to **SQLite** (`db.sqlite3`) for easier local testing.

3. **Run Tests**
   ```bash
   python manage.py test apps.accounts apps.shops apps.products apps.transactions apps.payments
   ```

## API Structure
- `/api/auth/` - Registration, JWT Login, Profile.
- `/api/shops/` - Shop and Branch management.
- `/api/products/` - Inventory and Categories.
- `/api/transactions/` - POS transactions (nested items supported).
- `/api/payments/` - M-Pesa configuration.
- `/api/accounting/` - Journal entries and reports.

## Troubleshooting
- **Permission Denied**: If `entrypoint.sh` fails, run `chmod +x scripts/entrypoint.sh` on your host.
- **DB Connection**: Ensure the `db` service is healthy in `docker compose ps`.
