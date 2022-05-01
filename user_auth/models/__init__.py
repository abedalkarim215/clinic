from .UserModels import User
from .DoctorModels import (
    Doctor,
    Education,
    WorkExperience,
)
from .PatientModels import (
    Patient,
    MedicalHistory,

)
__all__ = [
    #User Models
    User,

    #Patient Models
    Patient,
    MedicalHistory,

    #Doctor Models
    Doctor,
    Education,
    WorkExperience,

]