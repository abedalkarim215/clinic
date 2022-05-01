from rest_framework import serializers
from ..models import (
User,
Patient,
MedicalHistory,
)

class PatientGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'birthday',
            'gender',
            'image',
            'about_me',
            'location',
            'personal_phone_number',
        ]
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'birthday': {'required': False},
            'gender': {'required': False},
            'image': {'required': False},
            'about_me': {'required': False},
            'location': {'required': False},
            'personal_phone_number': {'required': False},
        }

class PatientMedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = [
            'id',
            'title',
            'time_period',
            'body',
        ]

class PatientProfileInfoSerializer(serializers.ModelSerializer):
    general = serializers.SerializerMethodField('get_general')
    medical_histories = serializers.SerializerMethodField('get_medical_histories')

    def get_general(self, obj):
        return PatientGeneralInfoSerializer(obj, context=self.context).data

    def get_medical_histories(self, obj):
        medical_histories = obj.patient.medicalhistory_set.all()
        return PatientMedicalHistorySerializer(medical_histories,many=True, context=self.context).data

    class Meta:
        model = User
        fields = [
            'general',
            'medical_histories',
        ]
