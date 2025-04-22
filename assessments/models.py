from django.db import models
from courses.models import Course, Assignment


class Question(models.Model):
    data = models.JSONField(default=list)
    create_date = models.DateTimeField(auto_now_add=True)
    creator = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Attempt(models.Model):
    data = models.JSONField(default=dict)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False)
    user = models.CharField(max_length=100)
    task = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.IntegerField(null=True, blank=True)
