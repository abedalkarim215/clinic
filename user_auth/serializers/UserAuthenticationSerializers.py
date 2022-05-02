from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from ..models import (
User,
Doctor,
Patient,
)

class RegisterSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(['Doctor','Patient'])
    password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)
    class Meta:
        model = User
        fields = [
            'type',
            'email',
            'password',
            'confirm_password',
        ]
        extra_kwargs = {
            'type': {'required': True},
            'email': {'required': True},
            'password': {
                'write_only': True,
                'required': True
            },
            'confirm_password': {
                'write_only': True,
                'required': True
            },
        }

    def create(self, validated_data):
        type = validated_data['type']
        email = validated_data['email']
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']

        if password == "":
            msg = _('يرجى إدخال كلمة المرور')
            raise serializers.ValidationError(msg, code='authorization')

        if password != confirm_password :
            msg = _('كلمات المرور المدخلة غير متطابقة.')
            raise serializers.ValidationError(msg, code='authorization')


        if len(password) < 8 :
            msg = _('كلمة المرور قصيرة جدا ، يجب أن لا تقل كلمة المرور عن 8 حروف أو أرقام.')
            raise serializers.ValidationError(msg, code='authorization')

        user = User.objects.create_user(
                                        email=email,
                                        password=password,
        )

        if user:
            if type == 'Doctor':
                profile = Doctor.objects.create(
                    user=user,
                )
            elif type == 'Patient':
                profile = Patient.objects.create(
                    user=user
                )
            else:
                msg = _('لم يتم التسجيل.')
                raise serializers.ValidationError(msg, code='authorization')
            return user

        else:
            msg = _('لم يتم التسجيل.')
            raise serializers.ValidationError(msg, code='authorization')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'account_photo',
            'email',
        ]

class UserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'account_type',
            'email',
            'first_name',
            'last_name',
            'location',
            'image',
            'gender',
            'birthday',
        ]
