from django.urls import path, include
from rest_framework import routers
from courses import views

router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'lectures', views.LectureViewSet)
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'submissions', views.SubmissionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]