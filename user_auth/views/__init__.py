from .UserAuthenticationViews import (
    RegisterAPI,
    LoginAPI,
    change_password,
    UserBasicInfo,
    UserProfileInfo


)
from .DoctorViews import (
    DoctorEditGeneralInfo,
    DoctorEditPersonalInfo,
    DoctorEditEducationInfo,
    DoctorEditWorkExperience,
    DoctorCreateWorkExperience,
)

from .PatientViews import (
PatientEditGeneralInfo,

)
__all__ = [
    #User Authentication Views
    RegisterAPI,
    LoginAPI,
    change_password,

    #User Views
    UserBasicInfo,
    UserProfileInfo,

    #Doctor Views
    DoctorEditGeneralInfo,
    DoctorEditPersonalInfo,
    DoctorEditEducationInfo,
    DoctorEditWorkExperience,
    DoctorCreateWorkExperience,

    #Patient Views
    PatientEditGeneralInfo,
]