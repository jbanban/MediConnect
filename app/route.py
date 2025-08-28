from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import datetime


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

#  Patients - View all doctors
@app.get("/api/doctors")
def get_all_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    return {
        "doctors": [
            {"id": d.id, "specialization": d.specialization, "contact": d.contact}
            for d in doctors
        ]
    }


#  Patients - View their own appointments
@app.get("/api/patients/{patient_id}/appointments")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter_by(patient_id=patient_id).all()
    return {
        "appointments": [
            {
                "id": a.id,
                "doctor_id": a.doctor_id,
                "schedule_id": a.schedule_id,
                "status": a.status,
                "reason": a.reason,
                "created_at": a.created_at,
            }
            for a in appointments
        ]
    }


#  Patients - Book an appointment
@app.post("/api/appointments")
def create_appointment(
    patient_id: int, doctor_id: int, schedule_id: int, reason: str = None, db: Session = Depends(get_db)
):
    # Check schedule availability
    schedule = db.query(Schedule).filter_by(id=schedule_id, status="Available").first()
    if not schedule:
        raise HTTPException(status_code=400, detail="Schedule not available")

    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        schedule_id=schedule_id,
        reason=reason,
        status="Pending",
        created_at=datetime.utcnow(),
    )

    db.add(appointment)
    schedule.status = "Booked"
    db.commit()
    db.refresh(appointment)

    return {"message": "Appointment booked successfully", "appointment_id": appointment.id}


#  Doctors - View their schedules
@app.get("/api/doctors/{doctor_id}/schedules")
def get_doctor_schedules(doctor_id: int, db: Session = Depends(get_db)):
    schedules = db.query(Schedule).filter_by(doctor_id=doctor_id).all()
    return {
        "schedules": [
            {
                "id": s.id,
                "date": s.date,
                "start_time": s.start_time,
                "end_time": s.end_time,
                "status": s.status,
            }
            for s in schedules
        ]
    }


#  Doctors - View their appointments
@app.get("/api/doctors/{doctor_id}/appointments")
def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter_by(doctor_id=doctor_id).all()
    return {
        "appointments": [
            {
                "id": a.id,
                "patient_id": a.patient_id,
                "schedule_id": a.schedule_id,
                "status": a.status,
                "reason": a.reason,
            }
            for a in appointments
        ]
    }



@app.get("/api/admin/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {
        "users": [
            {"id": u.id, "name": u.name, "email": u.email, "role": u.role}
            for u in users
        ]
    }


# Admin - List all appointments
@app.get("/api/admin/appointments")
def list_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return {
        "appointments": [
            {
                "id": a.id,
                "patient_id": a.patient_id,
                "doctor_id": a.doctor_id,
                "schedule_id": a.schedule_id,
                "status": a.status,
            }
            for a in appointments
        ]
    }
