from fastapi import FastAPI
from model import db

app = FastAPI

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