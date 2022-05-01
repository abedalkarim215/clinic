from rest_framework.permissions import BasePermission



class IsDoctor(BasePermission):
    message = 'User type Must Be Doctor'

    def has_permission(self, request, view):
        try:
            user = request.user.doctor
        except:
            return False
        return True

class IsPatient(BasePermission):
    message = 'User type Must Be Patient'

    def has_permission(self, request, view):
        try:
            user = request.user.patient
        except:
            return False
        return True