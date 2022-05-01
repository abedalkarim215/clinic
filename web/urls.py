from django.urls import path
from .views import Departments
urlpatterns = [
    path('get/departments/', Departments.as_view()),

]
