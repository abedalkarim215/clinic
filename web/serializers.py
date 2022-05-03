from rest_framework import serializers
from django.core.files.storage import FileSystemStorage
from datetime import datetime

from .models import (
    Department,
    Question,
    File,
    QuestionFile,
    Discussion,
    BlogFile,
    Blog,
    Comment,
)


def get_upload_file_path(type, filename):
    print(datetime.today().date())
    return 'files/{date}/{type}/{filename}'.format(
        date=datetime.today().date(),
        type=type,
        filename=filename
    )


def upload_files(files, model_name, model_object):
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
            if model_name == 'Question':
                question_file = QuestionFile.objects.create(
                    question=model_object,
                    file=file_object,
                )
            elif model_name == 'Blog':
                blog_file = BlogFile.objects.create(
                    blog=model_object,
                    file=file_object,
                )
        else:
            print(f"ERROR - > File did not uploaded sucessfuly :{file.name}")


def get_upload_discussion_file_path(user, filename):
    return 'discussions/files/{date}/{user}/{filename}'.format(
        date=datetime.today().date(),
        user=user.email_as_string(),
        filename=filename
    )


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class QuestionSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.FileField(), required=False)
    patient_image = serializers.SerializerMethodField('get_patient_image_full_url')

    def get_patient_image_full_url(self, obj):
        patient_image = obj.patient_image()
        request = self.context.get('request')
        return request.build_absolute_uri(patient_image)

    class Meta:
        model = Question
        fields = [
            'id',
            'patient',
            'patient_image',
            'patient_full_name',
            'title',
            'body',
            'to_doctor',
            'department',
            'files',
            'discussions_count',
            'created_at',
        ]
        extra_kwargs = {
            'title': {'required': True},
            'body': {'required': True},
            'to_doctor': {'required': False},
            'department': {'required': False},
            'files': {'required': False},
        }
        read_only_fields = [
            'id',
            'created_at',
            'patient',
            'patient_image',
            'patient_full_name',
            'discussions_count',
        ]

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
                upload_files(files=value, model_name='Question', model_object=instance)
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
            upload_files(files=files, model_name='Question', model_object=question)
            return question
        else:
            msg = 'لم يتم الإنشاء.'
            raise serializers.ValidationError(msg, code='authorization')


class DiscussionSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField('get_user_image_full_url')

    def get_user_image_full_url(self, obj):
        user_image = obj.user_image()
        request = self.context.get('request')
        return request.build_absolute_uri(user_image)

    class Meta:
        model = Discussion
        fields = [
            'id',
            'user',
            'user_image',
            'user_full_name',
            'question',
            'body',
            'file',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'user', 'user_image', 'user_full_name']
        extra_kwargs = {
            'question': {'required': True},
            'body': {'required': True},
            'file': {'required': False},
        }

    def get_fields(self, *args, **kwargs):
        fields = super(DiscussionSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['question'].required = False
            fields['question'].read_only = True
            fields['body'].required = False
        return fields

    def create(self, validated_data):
        user = self.context['request'].user
        question = validated_data['question']
        if (not (user.account_type() == "Doctor")) and (not (user == question.patient.user)):
            msg = 'لا تملك صلاحية بالتعليق على هذا السؤال.'
            raise serializers.ValidationError(msg, code='authorization')
        body = validated_data['body']
        file = validated_data['file'] if 'file' in validated_data else None

        discussion = Discussion.objects.create(
            question=question,
            user=user,
            body=body,
        )
        if discussion:
            if file:
                fs = FileSystemStorage()
                filename = fs.save(get_upload_discussion_file_path(user, file.name), file)
                uploaded_file_url = fs.url(filename)
                file_url = str(uploaded_file_url)[7:]
                discussion.file = file_url
                discussion.save()
            return discussion
        else:
            msg = 'لم يتم الإنشاء.'
            raise serializers.ValidationError(msg, code='authorization')


class BlogSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.FileField(), required=False)
    doctor_image = serializers.SerializerMethodField('get_doctor_image_full_url')

    def get_doctor_image_full_url(self, obj):
        doctor_image = obj.doctor_image()
        request = self.context.get('request')
        return request.build_absolute_uri(doctor_image)

    class Meta:
        model = Blog
        fields = [
            'id',
            'doctor',
            'doctor_image',
            'doctor_full_name',
            'title',
            'body',
            'files',
            'likes_count',
            'comments_count',
            'created_at',
        ]
        extra_kwargs = {
            'title': {'required': True},
            'body': {'required': True},
            'files': {'required': False},
        }
        read_only_fields = [
            'id',
            'created_at',
            'doctor',
            'doctor_image',
            'doctor_full_name',
            'likes_count',
            'comments_count',
        ]

    def get_fields(self, *args, **kwargs):
        fields = super(BlogSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['title'].required = False
            fields['body'].required = False
        return fields

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr in ['files']:
                # delete old blog files
                old_blog_files = instance.blogfile_set.all().delete()

                # upload new blog files
                upload_files(files=value, model_name='Blog', model_object=instance)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):

        doctor = self.context['request'].user.doctor
        title = validated_data['title']
        body = validated_data['body']

        blog = Blog.objects.create(
            doctor=doctor,
            title=title,
            body=body,
        )
        if blog:
            files = validated_data['files'] if 'files' in validated_data else []
            upload_files(files=files, model_name='Blog', model_object=blog)
            return blog
        else:
            msg = 'لم يتم الإنشاء.'
            raise serializers.ValidationError(msg, code='authorization')


class CommentSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField('get_user_image_full_url')

    def get_user_image_full_url(self, obj):
        user_image = obj.user_image()
        request = self.context.get('request')
        return request.build_absolute_uri(user_image)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'user_image',
            'user_full_name',
            'blog',
            'body',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'user', 'user_image', 'user_full_name']
        extra_kwargs = {
            'blog': {'required': True},
            'body': {'required': True},
        }

    def get_fields(self, *args, **kwargs):
        fields = super(CommentSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['blog'].required = False
            fields['blog'].read_only = True
        return fields

    def create(self, validated_data):
        user = self.context['request'].user
        blog = validated_data['blog']
        body = validated_data['body']

        comment = Comment.objects.create(
            blog=blog,
            user=user,
            body=body,
        )

        if comment:
            return comment
        else:
            msg = 'لم يتم الإنشاء.'
            raise serializers.ValidationError(msg, code='authorization')
