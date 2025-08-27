from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from fastapi import FastAPI

db = SQLAlchemy()

# User model (for patients and doctors login)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "patient" or "doctor"

    # Relationships
    patient_profile = db.relationship('Patient', backref='user', uselist=False)
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)


# Patient profile (extra info for patients)
class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    contact = db.Column(db.String(20), nullable=True)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)


# Doctor profile (extra info for doctors)
class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=True)

    schedules = db.relationship('Schedule', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)


# Doctor schedules (available times doctors provide)
class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Available')  
    appointments = db.relationship('Appointment', backref='schedule', lazy=True)


# Appointment booking by patient
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default='Pending')  # Pending / Confirmed / Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.get("/")
def index():
    return {"message": "Welcome to CurrentCare System"}

# ---------- PATIENT INTERFACE ----------
@app.get("/patient/dashboard")
def patient_dashboard():
    return {"message": "Patient Dashboard"}

@app.get("/patient/doctors")
def view_doctors():
    return {"message": "List of doctors"}

@app.get("/patient/appointments")
def view_appointment_records():
    return {"message": "Patient appointment records"}

@app.post("/patient/appointments")
def set_appointment():
    return {"message": "Set an appointment"}

@app.get("/patient/profile")
def patient_profile():
    return {"message": "Patient profile"}

@app.get("/patient/logout")
def patient_logout():
    return {"message": "Patient logged out"}


# ---------- DOCTOR INTERFACE ----------
@app.get("/doctor/dashboard")
def doctor_dashboard():
    return {"message": "Doctor Dashboard"}

@app.get("/doctor/appointments")
def doctor_appointments():
    return {"message": "Appointments assigned to doctor"}

@app.get("/doctor/schedules")
def doctor_schedules():
    return {"message": "Doctor schedules"}

@app.get("/doctor/profile")
def doctor_profile():
    return {"message": "Doctor profile"}

@app.get("/doctor/logout")
def doctor_logout():
    return {"message": "Doctor logged out"}


# ---------- ADMIN INTERFACE ----------
@app.get("/admin/dashboard")
def admin_dashboard():
    return {"message": "Admin Dashboard"}

@app.get("/admin/users")
def manage_users():
    return {"message": "Manage all users (patients/doctors)"}

@app.get("/admin/appointments")
def manage_appointments():
    return {"message": "Manage all appointments"}

@app.get("/admin/reports")
def admin_reports():
    return {"message": "Admin reports"}

@app.get("/admin/logout")
def admin_logout():
    return {"message": "Admin logged out"}