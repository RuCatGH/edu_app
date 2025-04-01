from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # ==================== Auth Endpoints ====================
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # ==================== Main Endpoints ====================
    path('', include("courses.urls", namespace="courses")),
    path('', include("assessments.urls", namespace="assessments"))
]
