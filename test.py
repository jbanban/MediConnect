from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    status = db.Column(db.String(20), default='Available')  # Available / Fully Booked

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
