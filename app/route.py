from fastapi import APIRouter
from app.components.doctor import doctor_router



api_router = APIRouter()


api_router.include_router(doctor_router)
