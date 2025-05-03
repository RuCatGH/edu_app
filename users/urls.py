from django.urls import path

from users.views import AddUserToCourseView, DeleteUserToCourseView, UpdateUserToCourseView

app_name = 'users'

urlpatterns = [
    path('course/user/add/', AddUserToCourseView.as_view(), name='course_user_add'),
    path('course/user/delete/', DeleteUserToCourseView.as_view(), name='course_user_delete'),
    path('course/user/update/', UpdateUserToCourseView.as_view(), name='course_user_update'),
]