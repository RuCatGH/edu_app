from rest_framework import serializers
from .models import Course, Lecture, Assignment


class CourseSerializer(serializers.ModelSerializer):
    createDate = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    lectures = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'createDate',
                  'users', 'owner', 'lectures', 'tasks']

    def get_createDate(self, obj):
        return int(obj.create_date.timestamp())

    def get_users(self, obj):
        return [obj.students, obj.teachers]

    def get_lectures(self, obj):
        return list(obj.lecture_set.values_list('id', flat=True))

    def get_tasks(self, obj):
        return list(obj.assignment_set.values_list('id', flat=True))


class LectureSerializer(serializers.ModelSerializer):
    createDate = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = ['id', 'title', 'data', 'createDate',
                  'active', 'creator', 'users', 'course']

    def get_createDate(self, obj):
        return int(obj.create_date.timestamp())

    def get_users(self, obj):
        return obj.users_access


class AssignmentSerializer(serializers.ModelSerializer):
    createDate = serializers.SerializerMethodField()
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    attempts = serializers.IntegerField(source='attempts_allowed')

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'data', 'createDate', 'active',
                  'attempts', 'startDate', 'endDate', 'creator', 'users', 'course']

    def get_createDate(self, obj):
        return int(obj.create_date.timestamp())

    def get_startDate(self, obj):
        return int(obj.start_date.timestamp()) if obj.start_date else -1

    def get_endDate(self, obj):
        return int(obj.end_date.timestamp()) if obj.end_date else -1

    def get_users(self, obj):
        return obj.users_access


class CourseUserSerializer(serializers.Serializer):
    course = serializers.IntegerField()
    user = serializers.CharField()
    # 0 for student, 1 for moderator
    role = serializers.IntegerField(required=False)
