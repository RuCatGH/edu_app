from django.urls import path, include
from . import views

app_name = 'assessments'

urlpatterns = [
    # ==================== Question Endpoints ====================
    path('question/create', views.QuestionCreateAPIView.as_view(), name='question-create'),
    path('question/update', views.QuestionUpdateAPIView.as_view(), name='question-update'),
    path('question/get', views.QuestionGetAPIView.as_view(), name='question-get'),

    # ==================== Attempt Endpoints ====================
    path('attempts/<int:attemptId>/grade', views.AttemptGradeAPIView.as_view(), name='attempt-grade'),
    path('attempts/', views.AttemptListAPIView.as_view(), name='attempt-list'),
    path('attempts/create', views.AttemptCreateAPIView.as_view(), name='attempt-create'),
    path('attempts/<int:attemptId>', views.AttemptUpdateAPIView.as_view(), name='attempt-update'),
    path('attempts/<int:attemptId>/finish', views.AttemptFinishAPIView.as_view(), name='attempt-finish'),
]