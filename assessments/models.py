from django.db import models
from django.contrib.auth.models import User

from courses.models import Course, Assignment


class Question(models.Model):
    data = models.JSONField(default=list)  # Список версий вопроса
    create_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Attempt(models.Model):
    data = models.JSONField(default=dict)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.IntegerField(null=True, blank=True)
