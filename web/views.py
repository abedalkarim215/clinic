from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from user_auth.permissions import IsDoctor,IsPatient
from .models import (
    Department,
)


class Departments(generics.ListAPIView):
    from .serializers import DepartmentSerializer
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated,IsDoctor|IsPatient]
    pagination_class = None

    def get_queryset(self):
        # departmets_test_lest = ["COVID-19",
        #  "Allergist",
        #  "Anesthesiologist-resuscitator",
        #  "Venereologist",
        #  "Gastroenterologist",
        #  "Hematologist",
        #  "Geneticist",
        #  "Hepatologist",
        #  "Gynecologist",
        #  "Homeopathist",
        #  "Dermatologist",
        #  "Pediatric gastroenterologist",
        #  "Pediatric gynecologist",
        #  "Children's dermatologist",
        #  "Children's infectious disease specialist",
        #  "Pediatric cardiologist",
        #  "Children's ENT",
        #  "Children's neurologist",
        #  "Pediatric Nephrologist",
        #  "Children's ophthalmologist",
        #  "Child psychologist",
        #  "Children's pulmonologist",
        #  "Pediatric rheumatologist",
        #  "Pediatric urologist",
        #  "Pediatric surgeon",
        #  "Pediatric endocrinologist",
        #  "Nutritionist",
        #  "Immunologist",
        #  "Infectionist",
        #  "Cardiologist",
        #  "Clinical psychologist",
        #  "Clinical psychologist",
        #  "Cosmetologist",
        #  "Speech therapist",
        #  "Lore",
        #  "Medical lawyer",
        #  "Mammologist",
        #  "Expert in narcology"]
        # for departmet in departmets_test_lest :
        #     new_department = Department.objects.create(name=departmet)
        departments = Department.objects.all()
        return departments
