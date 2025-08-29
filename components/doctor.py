from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.model import Schedule, Appointment

doctor_router = APIRouter(prefix="/doctor", tags=["Doctor"])

@doctor_router.get("/dashboard")
def doctor_dashboard():
    return {"message": "Doctor Dashboard"}

@doctor_router.get("/{doctor_id}/schedules")
def doctor_schedules(doctor_id: int, db: Session = Depends(get_db)):
    return db.query(Schedule).filter_by(doctor_id=doctor_id).all()

@doctor_router.get("/{doctor_id}/appointments")
def doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    return db.query(Appointment).filter_by(doctor_id=doctor_id).all()
