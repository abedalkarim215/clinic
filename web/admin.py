from django.contrib import admin
from .models import (
                    Question,
                    Discussion,
                    Blog,
                    Comment,
                    BlogLike,
                    File,
                    QuestionFile,
                    DiscussionFile,
                    BlogFile,
                    Department,
)

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('id','username','email','full_name','mobile')
#
#     def email(self,instance):
#         try:
#             return instance.user.email
#         except :
#             return 'ERROR!!'
#
#

admin.site.register(Question)
admin.site.register(Discussion)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(BlogLike)
admin.site.register(File)
admin.site.register(QuestionFile)
admin.site.register(DiscussionFile)
admin.site.register(BlogFile)
admin.site.register(Department)


