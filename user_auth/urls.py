from django.urls import path
from knox import views as knox_views
from .views import (
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
                    )

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
    path('change/password/', change_password),

    #User API's
    path('user/get/basic/info/', UserBasicInfo.as_view()),
    path('user/get/profile/info/', UserProfileInfo.as_view()),


    #Doctor API's
    path('doctor/edit/general/info/', DoctorEditGeneralInfo.as_view()),
    path('doctor/edit/personal/info/', DoctorEditPersonalInfo.as_view()),
    path('doctor/edit/education/info/', DoctorEditEducationInfo.as_view()),
    path('doctor/edit/work/experience/', DoctorEditWorkExperience.as_view()),
    path('doctor/create/work/experience/', DoctorCreateWorkExperience.as_view()),

    # Patient API's
    path('patient/edit/general/info/', PatientEditGeneralInfo.as_view()),
]
