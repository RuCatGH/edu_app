from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course

User = get_user_model()

class AddUpdateUserSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=False, write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    role = serializers.ChoiceField(choices=[(0, "student"), (1, "teacher")], write_only=True)

class DeleteUserSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=False, write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)

