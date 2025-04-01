from rest_framework import serializers
from .models import Course, Question, Attempt
from django.contrib.auth.models import User

class QuestionSerializer(serializers.ModelSerializer):
    createDate = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'data', 'createDate', 'creator', 'course']

    def get_createDate(self, obj):
        return int(obj.create_date.timestamp())

class AttemptSerializer(serializers.ModelSerializer):
    startDate = serializers.SerializerMethodField()
    endDate = serializers.SerializerMethodField()

    class Meta:
        model = Attempt
        fields = ['id', 'data', 'startDate', 'endDate', 'finished', 'user', 'task', 'course', 'grade']

    def get_startDate(self, obj):
        return int(obj.start_date.timestamp())

    def get_endDate(self, obj):
        return int(obj.end_date.timestamp()) if obj.end_date else -1