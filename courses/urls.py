from django.urls import path, include
from . import views

urlpatterns = [
    # ==================== Course Endpoints ====================
    path('course/create', views.CourseCreateAPIView.as_view()),
    path('course/update', views.CourseUpdateAPIView.as_view()),
    path('course/delete', views.CourseDeleteAPIView.as_view()),
    path('course/get', views.CourseGetAPIView.as_view()),

    # ==================== Lecture Endpoints ====================
    path('lecture/create', views.LectureCreateAPIView.as_view()),
    path('lecture/update', views.LectureUpdateAPIView.as_view()),
    path('lecture/delete', views.LectureDeleteAPIView.as_view()),
    path('lecture/get', views.LectureGetAPIView.as_view()),

    # ==================== Assignment Endpoints ====================
    path('task/create', views.AssignmentCreateAPIView.as_view()),
    path('task/update', views.AssignmentUpdateAPIView.as_view()),
    path('task/get', views.AssignmentGetAPIView.as_view()),

    # ==================== Question Endpoints ====================
    path('question/create', views.QuestionCreateAPIView.as_view()),
    path('question/update', views.QuestionUpdateAPIView.as_view()),
    path('question/get', views.QuestionGetAPIView.as_view()),

    # ==================== Attempt Endpoints ====================
    path('attempts/<int:attemptId>/grade', views.AttemptGradeAPIView.as_view()),
    path('attempts/', views.AttemptListAPIView.as_view()),
    path('attempts/create', views.AttemptCreateAPIView.as_view()),
    path('attempts/<int:attemptId>', views.AttemptUpdateAPIView.as_view()),
    path('attempts/<int:attemptId>/finish',
         views.AttemptFinishAPIView.as_view()),

    # ==================== Auth Endpoints ====================
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
