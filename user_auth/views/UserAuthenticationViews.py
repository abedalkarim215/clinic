from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import serializers
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from knox.views import LoginView as KnoxLoginView
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from ..permissions import IsDoctor,IsPatient
from ..models import (
User,
)


class RegisterAPI(generics.GenericAPIView):
    from ..serializers.UserAuthenticationSerializers import RegisterSerializer
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        from ..serializers.UserAuthenticationSerializers import UserSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            check_user = get_object_or_404(User,email=email)
        except:
            msg = _('البريد الإلكتروني المدخل غير صحيح.')
            raise serializers.ValidationError(msg, code='authorization')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('كلمة المرور المدخلة غير صحيحة')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('يرجى التأكد من إدخال البريد الإلكتروني وكلمة المرور.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs




class LoginAPI(KnoxLoginView):
    permission_classes = [AllowAny]
    template_name = 'user_auth/login_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, format=None):
        serializer = MyAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
        #return HttpResponseRedirect('http://localhost:3000/')



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request) :
    try:
        user = User.objects.get(pk=request.user.id)
    except:
        return JsonResponse(status=404,data={'status':False,"message": "User Not Found"})
    try:
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
    except:
        msg = _('يرجى التأكد من إدخال جميع الحقول.')
        raise serializers.ValidationError(msg, code='authorization')

    if not user.check_password(old_password):
        msg = _('كلمة المرور القديمة المدخلة غير صحيحة')
        raise serializers.ValidationError(msg, code='authorization')
    elif new_password != confirm_new_password :
        msg = _('كلمات المرور المدخلة غير متطابقة.')
        raise serializers.ValidationError(msg, code='authorization')
    if len(new_password) < 8 :
        msg = _('كلمة المرور قصيرة جدا ، يجب أن لا تقل كلمة المرور عن 8 حروف أو أرقام.')
        raise serializers.ValidationError(msg, code='authorization')
    elif old_password == new_password :
        msg = _('كلمة المرور القديمة لا يمكن أن تكون هي كلمة المرور الجديدة، يرجى إختيار كلمة أخرى.')
        raise serializers.ValidationError(msg, code='authorization')
    else :
        user.set_password(new_password)
        user.save()
        # update_session_auth_hash(request, user)
        return JsonResponse(status=201,data={'status':True,"message": "تم تغيير كلمة المرور بنجاح"})


class UserBasicInfo(generics.RetrieveAPIView):
    from ..serializers import UserBasicInfoSerializer
    serializer_class = UserBasicInfoSerializer
    permission_classes = [IsAuthenticated, IsDoctor|IsPatient]

    def get_object(self):
        return self.request.user

class UserProfileInfo(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsDoctor|IsPatient]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.account_type() == "Doctor" :
            from ..serializers import DoctorProfileInfoSerializer
            serializer = DoctorProfileInfoSerializer(instance,context={'request':self.request})
            return Response(serializer.data)
        elif self.request.user.account_type() == "Patient" :
            from ..serializers import PatientProfileInfoSerializer
            serializer = PatientProfileInfoSerializer(instance,context={'request':self.request})
            return Response(serializer.data)
        else :
            return None