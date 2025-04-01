from rest_framework import serializers
from .models import Course, Lecture, Assignment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CourseSerializer(serializers.ModelSerializer):
    createDate = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    lectures = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'createDate', 'users', 'owner', 'lectures', 'tasks']

    def get_createDate(self, obj):
        return int(obj.create_date.timestamp())

    def get_users(self, obj):
        students = obj.students.all().values_list('id', flat=True)
        teachers = obj.teachers.all().values_list('id', flat=True)
        return [list(students), list(teachers)]

    def get_lectures(self, obj):
        return list(obj.lecture_set.values_list('id', flat=True))

    def get_tasks(self, obj):
        return list(obj.assignment_set.values_list('id', flat=True))

class LectureSerializer(serializers.ModelSerializer):
    createDate = serializers.SerializerMethodField()
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    users = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = ['id', 'title', 'data', 'createDate', 'active', 'creator', 'users', 'course']

    def get_createDate(self, obj):
        return int(obj.create_date.timestamp())

    def get_users(self, obj):
        return obj.users_access

class AssignmentSerializer(serializers.ModelSerializer):
    createDate = serializers.SerializerMethodField()
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'data', 'createDate', 'active', 'attempts_allowed', 'startDate', 'endDate', 'creator', 'users', 'course']

    def get_createDate(self, obj):
        return int(obj.create_date.timestamp())

    def get_startDate(self, obj):
        return int(obj.start_date.timestamp()) if obj.start_date else -1

    def get_endDate(self, obj):
        return int(obj.end_date.timestamp()) if obj.end_date else -1

    def get_users(self, obj):
        return obj.users_access