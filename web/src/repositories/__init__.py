from .order import OrderRepository
from .result import ResultRepository
from .doctor import DoctorRepository
from .patient import PatientRepository
from .service import ServiceRepository
from .speciality import SpecialityRepository
from .appointment import AppointmentRepository
from .device import DeviceRepository
from .prediction import PredictionRepository

__all__ = [
    "OrderRepository", 
    "ResultRepository", 
    "DoctorRepository", 
    "PatientRepository", 
    "ServiceRepository", 
    "SpecialityRepository", 
    "AppointmentRepository",
    "DeviceRepository",
    "PredictionRepository"
    ]    
