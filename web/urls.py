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
    BlogDetails,
    BlogComments,
    CreateBlog,
    EditBlog,
    DeleteBlog,
    CreateComment,
    EditComment,
    DeleteComment,
    BlogLike,
    DepartmentQuestions,
    DepartmentsDoctors,
    PersonalQuestions,
)

urlpatterns = [
    path('media/files/<path:file>', dummy_secure_media_directory),

    path('get/departments/', Departments.as_view()),
    path('get/departments/doctors/', DepartmentsDoctors.as_view()),

    path('get/question/details/', QuestionDetails.as_view()),
    path('get/question/discussions/', QuestionDiscussions.as_view()),
    path('get/department/questions/', DepartmentQuestions.as_view()),
    path('get/personal/questions/', PersonalQuestions.as_view()),

    path('create/question/', CreateQuestion.as_view()),
    path('edit/question/', EditQuestion.as_view()),
    path('delete/question/', DeleteQuestion.as_view()),

    path('create/discussion/', CreateDiscussion.as_view()),
    path('edit/discussion/', EditDiscussion.as_view()),
    path('delete/discussion/', DeleteDiscussion.as_view()),

    path('get/blog/details/', BlogDetails.as_view()),
    path('get/blog/comments/', BlogComments.as_view()),
    path('create/blog/', CreateBlog.as_view()),
    path('edit/blog/', EditBlog.as_view()),
    path('delete/blog/', DeleteBlog.as_view()),

    path('create/comment/', CreateComment.as_view()),
    path('edit/comment/', EditComment.as_view()),
    path('delete/comment/', DeleteComment.as_view()),

    path('blog/like/', BlogLike.as_view()),

]
