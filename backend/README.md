# Backend Setup & Run Guide

## Prerequisites

- Python 3.11+
- PostgreSQL (matching settings in .env)
- Redis
- (Optional) Python venv

## 1. Install Dependencies

cd appifylabTask/backend
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

## 2. Configure Environment

Create a `.env` file in backend/ using `.env.example` as a reference.

## 3. Apply Database Migrations

alembic upgrade head

## 4. Run the API

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## 5. Verify

Open: http://localhost:8000/docs
