from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from courses.models import Course
from .serializers import AddUpdateUserSerializer, DeleteUserSerializer

class AddUserToCourseView(CreateAPIView):
    serializer_class = AddUpdateUserSerializer
    queryset = Course.objects.all()

    def create(self, request, *args, **kwargs):
        serializer: AddUpdateUserSerializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data["course"]
        user = serializer.validated_data["user"]
        role = serializer.validated_data["role"]

        if role == 0:
            if course.teachers.filter(id=user.id).exists():
                raise ValidationError("Пользователь находится в списке преподавателей")
            course.students.add(user)
        else:
            if course.students.filter(id=user.id).exists():
                raise ValidationError("Пользователь находится в списке студентов")
            course.teachers.add(user)

        return Response(serializer.data)


class DeleteUserToCourseView(DestroyAPIView):
    serializer_class = DeleteUserSerializer
    queryset = Course.objects.all()

    def create(self, request, *args, **kwargs):
        serializer: DeleteUserSerializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data["course"]
        user = serializer.validated_data["user"]

        course.students.remove(user)
        course.teachers.remove(user)

        return Response(serializer.data)


class UpdateUserToCourseView(UpdateAPIView):
    serializer_class = AddUpdateUserSerializer
    queryset = Course.objects.all()
    http_method_names = ["put"]

    def put(self, request, *args, **kwargs):
        serializer: AddUpdateUserSerializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data["course"]
        user = serializer.validated_data["user"]
        role = serializer.validated_data["role"]

        if role == 0:
            course.teachers.remove(user)
            course.students.add(user)
        else:
            course.students.remove(user)
            course.teachers.add(user)

        return Response(serializer.data)