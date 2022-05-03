from django.urls import path
from .views import (
    Departments,
    QuestionDetails,
    QuestionDiscussions,
    CreateQuestion,
    EditQuestion,
    dummy_secure_media_directory,
    CreateDiscussion,
    EditDiscussion,
    DeleteQuestion,
    DeleteDiscussion,
)
urlpatterns = [
    path('get/departments/', Departments.as_view()),


    path('get/question/details/', QuestionDetails.as_view()),
    path('get/question/discussions/', QuestionDiscussions.as_view()),
    path('create/question/', CreateQuestion.as_view()),
    path('edit/question/', EditQuestion.as_view()),
    path('delete/question/', DeleteQuestion.as_view()),
    path('media/files/<path:file>', dummy_secure_media_directory),

    path('create/discussion/', CreateDiscussion.as_view()),
    path('edit/discussion/', EditDiscussion.as_view()),
    path('delete/discussion/', DeleteDiscussion.as_view()),
]
