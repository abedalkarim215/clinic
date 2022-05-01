from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsPatient
from ..models import (
    User,
    Patient,
)



class PatientEditGeneralInfo(generics.UpdateAPIView):
    from ..serializers import PatientGeneralInfoSerializer
    serializer_class = PatientGeneralInfoSerializer
    permission_classes = [IsAuthenticated,IsPatient]
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj