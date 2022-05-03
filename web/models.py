from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime

class Department(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

class Question(models.Model):
    patient = models.ForeignKey('user_auth.Patient',on_delete= models.CASCADE)
    title = models.CharField(max_length=255,null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    to_doctor = models.ForeignKey('user_auth.Doctor',null=True,blank=True,on_delete=models.SET_NULL)
    department = models.ForeignKey('web.Department',null=True,blank=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def files(self):
        question_files = [file_path.path for file_path in File.objects.filter(id__in=list(self.questionfile_set.values_list('file_id',flat=True)))]
        return question_files

    def discussions(self):
        question_discussions = self.discussion_set.all()
        from .serializers import DiscussionSerializer
        return DiscussionSerializer(question_discussions,many=True).data
class Discussion(models.Model):
    def upload_discussion_file(self, filename):
        return 'discussions/files/{date}/{user}/{filename}'.format(
            date=datetime.today().date(),
            user=self.user.email_as_string(),
            filename=filename
        )
    question = models.ForeignKey('web.Question',on_delete= models.CASCADE)
    user = models.ForeignKey('user_auth.User', on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    file = models.FileField(
        upload_to=upload_discussion_file,
        default='/default_images/default_image_for_all_models.jpeg'
    )
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)

    def __str__(self):
        return self.user.email

class Blog(models.Model):
    doctor = models.ForeignKey('user_auth.Doctor',on_delete= models.CASCADE)
    title = models.CharField(max_length=255,null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)

    def __str__(self):
        return self.doctor.user.email

class Comment(models.Model):
    blog = models.ForeignKey('web.Blog',on_delete= models.CASCADE)
    user = models.ForeignKey('user_auth.User', on_delete=models.CASCADE)
    comment = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)

    def __str__(self):
        return self.user.email

class BlogLike(models.Model):
    blog = models.ForeignKey('web.Blog',on_delete= models.CASCADE)
    user = models.ForeignKey('user_auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)

    def __str__(self):
        return self.user.email

class File(models.Model):
    def upload_file(self, filename):
        return 'files/{date}/{type}/{filename}'.format(
            # user=patient.user.email_as_string(),
            date=datetime.today().date(),
            type=self.type,
            filename=filename
        )
    class Type(models.TextChoices):
        Image = "image", "Image"
        Video = "video", "Video"
        Voice = "audio", "Audio"
    path = models.FileField(
        upload_to=upload_file,
        default='/default_images/default_image_for_all_models.jpeg'
    )
    type = models.CharField(
        max_length=5,
        choices=Type.choices,
        default=Type.Image,
    )
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)

class QuestionFile(models.Model):
    question = models.ForeignKey('web.Question',on_delete= models.CASCADE)
    file = models.ForeignKey('web.File',on_delete= models.CASCADE)

    def __str__(self):
        return self.question.patient.user.email

# class DiscussionFile(models.Model):
#     discussion = models.ForeignKey('web.Discussion',on_delete= models.CASCADE)
#     file = models.ForeignKey('web.File',on_delete= models.CASCADE)
#
#     def __str__(self):
#         return self.discussion.user.email

class BlogFile(models.Model):
    blog = models.ForeignKey('web.Blog',on_delete= models.CASCADE)
    file = models.ForeignKey('web.File',on_delete= models.CASCADE)

    def __str__(self):
        return self.blog.doctor.user.email