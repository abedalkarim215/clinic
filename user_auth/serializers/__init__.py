from .UserAuthenticationSerializers import (
    RegisterSerializer,
    UserSerializer,
    UserBasicInfoSerializer,


)
from .DoctorSerializers import (
    DoctorProfileInfoSerializer,
    DoctorGeneralInfoSerializer,
    DoctorPersonalInfoSerializer,
    DoctorEducationInfoSerializer,
    DoctorWorkExperienceSerializer,



)

from.PatientSerializers import (
    PatientProfileInfoSerializer,
    PatientGeneralInfoSerializer,
    PatientMedicalHistorySerializer,
)
__all__ = [
    #User Authentication Serializers
    RegisterSerializer,
    UserSerializer,

    #User Serializers
    UserBasicInfoSerializer,

    #Doctor Serializers
    DoctorProfileInfoSerializer,
    DoctorGeneralInfoSerializer,
    DoctorPersonalInfoSerializer,
    DoctorEducationInfoSerializer,
    DoctorWorkExperienceSerializer,

    #DoctorEditGeneralInfoSerializer,

    # Patient Serializers
    PatientProfileInfoSerializer,
    PatientGeneralInfoSerializer,
    PatientMedicalHistorySerializer,
]