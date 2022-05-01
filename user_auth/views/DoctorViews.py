from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsDoctor
from rest_framework.response import Response
from ..models import (
    User,
    Doctor,
    Education,
    WorkExperience,
)

class DoctorEditGeneralInfo(generics.UpdateAPIView):
    from ..serializers import DoctorGeneralInfoSerializer
    serializer_class = DoctorGeneralInfoSerializer
    permission_classes = [IsAuthenticated,IsDoctor]
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class DoctorEditPersonalInfo(generics.UpdateAPIView):
    from ..serializers import DoctorPersonalInfoSerializer
    serializer_class = DoctorPersonalInfoSerializer
    permission_classes = [IsAuthenticated,IsDoctor]
    queryset = Doctor.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.doctor.id)
        self.check_object_permissions(self.request, obj)
        return obj

class DoctorEditEducationInfo(generics.UpdateAPIView):
    from ..serializers import DoctorEducationInfoSerializer
    serializer_class = DoctorEducationInfoSerializer
    permission_classes = [IsAuthenticated,IsDoctor]
    queryset = Education.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            doctor_education = self.request.user.doctor.education
        except:
            doctor_education = Education.objects.create(
                doctor=self.request.user.doctor,
            )
        obj = queryset.get(pk=doctor_education.id)
        self.check_object_permissions(self.request, obj)
        return obj

class DoctorEditWorkExperience(generics.UpdateAPIView):
    from ..serializers import DoctorWorkExperienceSerializer
    serializer_class = DoctorWorkExperienceSerializer
    permission_classes = [IsAuthenticated,IsDoctor]

    def get_object(self):
        try:
            work_experience_id = self.request.POST['id']
        except:
            return 0
        try:
            obj = self.request.user.doctor.workexperience_set.get(id=work_experience_id)
            print(obj)
        except:
            return 1
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance == 0:
            return Response({
                            'status':False,
                            'msg':"يرجى إرسال المعرف (id) الخاص بالعنصر المراد التعديل عليه",
                            },
                            status=400
                           )
        if instance == 1:
            return Response({
                            'status':False,
                            'msg':"العنصر الذي تحاول التعديل عليه غير موجود",
                            },
                            status=404
                           )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

class DoctorCreateWorkExperience(generics.CreateAPIView):
    from ..serializers import DoctorWorkExperienceSerializer
    serializer_class = DoctorWorkExperienceSerializer
    permission_classes = [IsAuthenticated,IsDoctor]