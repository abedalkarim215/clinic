from rest_framework import serializers
from django.core.files.storage import FileSystemStorage
from datetime import datetime

from .models import (
    Department,
    Question,
    File,
    QuestionFile,
    Discussion,
)


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id','name']

def get_upload_file_path(type, filename):
    print(datetime.today().date())
    return 'files/{date}/{type}/{filename}'.format(
        # user=patient.user.email_as_string(),
        date=datetime.today().date(),
        type=type,
        filename=filename
    )

def upload_files_for_question(files,question):
    for file in files:
        file_type = file.content_type.split('/')[0]
        fs = FileSystemStorage()
        filename = fs.save(get_upload_file_path(file_type, file.name), file)
        print(file.content_type)
        uploaded_file_url = fs.url(filename)
        file_url = str(uploaded_file_url)[7:]
        file_object = File.objects.create(
            type=file_type,
            path=file_url
        )
        if file_object:
            question_file = QuestionFile.objects.create(
                question=question,
                file=file_object,
            )
        else:
            print(f"ERROR - > File did not uploades :{file.name}")

class QuestionSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.FileField(),required=False)

    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'body',
            'to_doctor',
            'department',
            'files',
            # 'discussions',
            'created_at',
        ]
        extra_kwargs = {
            'title': {'required': True},
            'body': {'required': True},
            'to_doctor': {'required': False},
            'department': {'required': False},
            'files': {'required': False},
        }
        read_only_fields = ['id','created_at']

    def get_fields(self, *args, **kwargs):
        # fields = super(QuestionSerializer, self).get_fields(*args, **kwargs)
        fields = super(QuestionSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['title'].required = False
            fields['body'].required = False
        return fields
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr in ['files']:
                # delete old question files
                old_question_files = instance.questionfile_set.all().delete()

                # upload new question files
                upload_files_for_question(value,instance)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):

        patient = self.context['request'].user.patient
        title = validated_data['title']
        body = validated_data['body']
        to_doctor = validated_data['to_doctor'] if 'to_doctor' in validated_data else None
        department = validated_data['department'] if 'department' in validated_data else None

        question = Question.objects.create(
            patient=patient,
            title=title,
            body=body,
            to_doctor=to_doctor,
            department=department,
        )
        if question:
            files = validated_data['files'] if 'files' in validated_data else []
            upload_files_for_question(files, question)
            return question
        else:
            msg = 'لم يتم الإنشاء.'
            raise serializers.ValidationError(msg, code='authorization')

class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = [
            'id',
            'user',
            'body',
            'created_at',
        ]
        read_only_fields = ['id','created_at']
