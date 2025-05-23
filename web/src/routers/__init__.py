from .result import router as results_router
from .order import router as orders_router
from .doctor import router as doctors_router
from .patient import router as patients_router
from .service import router as services_router
from .speciality import router as specialities_router
from .appointment import router as appointments_router
from .device import router as devices_router
from .prediction import router as predictions_router
from fastapi import APIRouter


main_router = APIRouter()
main_router.include_router(results_router)
main_router.include_router(orders_router)
main_router.include_router(doctors_router)
main_router.include_router(patients_router)    
main_router.include_router(services_router)
main_router.include_router(specialities_router)
main_router.include_router(appointments_router)
main_router.include_router(devices_router)
main_router.include_router(predictions_router)
