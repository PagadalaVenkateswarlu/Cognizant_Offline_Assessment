# Event Slot Booking System

Object : This project is a slot booking system with:

    FastAPI backend (Python) – handles APIs and database

    AngularJS frontend – user interface for booking and admin

## Tech Stack
Frontend: Angular + Angular Material
Backend: FastAPI (Python)
Database: PostgreSQL

## Access:

Frontend: http://localhost:8080

Backend APIs: http://localhost:8000/docs

## Setup
## Run Both Backend + Frontend
## Frontend

cd Frontend
python -m http.server 8080

### Backend

cd Backend
uvicorn main:app --reload --port 8000

pip install -r requirements.txt


### Frontend

cd frontend
npm install
ng serve

App runs at

http://localhost:4200