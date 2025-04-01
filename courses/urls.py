from django.urls import path, include
from . import views

app_name = 'courses'

urlpatterns = [
    # ==================== Course Endpoints ====================
    path('course/create', views.CourseCreateAPIView.as_view(), name='course-create'),
    path('course/update', views.CourseUpdateAPIView.as_view(), name='course-update'),
    path('course/delete', views.CourseDeleteAPIView.as_view(), name='course-delete'),
    path('course/get', views.CourseGetAPIView.as_view(), name='course-get'),

    # ==================== Lecture Endpoints ====================
    path('lecture/create', views.LectureCreateAPIView.as_view(), name='lecture-create'),
    path('lecture/update', views.LectureUpdateAPIView.as_view(), name='lecture-update'),
    path('lecture/delete', views.LectureDeleteAPIView.as_view(), name='lecture-delete'),
    path('lecture/get', views.LectureGetAPIView.as_view(), name='lecture-get'),

    # ==================== Assignment Endpoints ====================
    path('task/create', views.AssignmentCreateAPIView.as_view(), name='task-create'),
    path('task/update', views.AssignmentUpdateAPIView.as_view(), name='task-update'),
    path('task/get', views.AssignmentGetAPIView.as_view(), name='task-get'),
]