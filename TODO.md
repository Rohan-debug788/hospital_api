# Hospital API Build Plan

## Steps to Complete

- [x] Create requirements.txt with necessary dependencies (Flask, Flask-SQLAlchemy, Flask-RESTful, Flask-JWT-Extended)
- [x] Fix app.py: Add return statement to create_app function
- [x] Define database models in models.py: User, Patient, Doctor, Appointment, Schedule
- [x] Implement authentication resources in auth.py: Register and Login endpoints with JWT
- [x] Implement appointment resources in appointment.py: CRUD operations for appointments
- [x] Implement schedule resources in schedule.py: CRUD operations for doctor schedules
- [x] Update app.py: Import Flask-RESTful and Flask-JWT-Extended, initialize them, register all API resources
- [ ] Install dependencies and test the API endpoints
