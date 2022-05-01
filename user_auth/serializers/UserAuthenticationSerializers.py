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
        # if type == "Doctor":
        #     personal_ID = validated_data['personal_ID']
        #     personal_ID_is_taken = Doctor.objects.filter(personal_ID=personal_ID).exists()
        #     if personal_ID_is_taken :
        #         msg = _('الرقم المدني المدخل مستخدم من قبل شخص أخر ، يرجى إدخال رقم آخر.')
        #         raise serializers.ValidationError(msg, code='authorization')

        # email_is_taken = User.objects.filter(email=email).exists()
        # if email_is_taken :
        #     msg = _('البريد الالكتروني المدخل مستخدم من قبل شخص أخر ، يرجى إدخال بريد إخر.')
        #     raise serializers.ValidationError(msg, code='authorization')

        if password == "":
            msg = _('يرجى إدخال كلمة المرور')
            raise serializers.ValidationError(msg, code='authorization')

        if password != confirm_password :
            msg = _('كلمات المرور المدخلة غير متطابقة.')
            raise serializers.ValidationError(msg, code='authorization')


        if len(password) < 8 :
            msg = _('كلمة المرور قصيرة جدا ، يجب أن لا تقل كلمة المرور عن 8 حروف أو أرقام.')
            raise serializers.ValidationError(msg, code='authorization')


        # personal_phone_number_is_taken = User.objects.filter(personal_phone_number=personal_phone_number).exists()
        # if personal_phone_number_is_taken :
        #     msg = _('رقم الهاتف المدخل مستخدم من قبل شخص أخر ، يرجى إدخال رقم آخر.')
        #     raise serializers.ValidationError(msg, code='authorization')
        #


        #image url settings
        # fs = FileSystemStorage()
        # filename = fs.save(upload_user_image(email_to_string(email),image.name), image)
        # uploaded_file_url = fs.url(filename)
        # image_url = str(uploaded_file_url)[6:]
        #end image url settings

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
