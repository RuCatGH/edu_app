from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User

from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_courses')
    teachers = models.ManyToManyField(
        User, related_name='taught_courses', blank=True)
    students = models.ManyToManyField(
        User, related_name='attended_courses', blank=True)
    tags = ArrayField(models.CharField(max_length=50),
                      blank=True, default=list)
    metadata = models.JSONField(default=dict)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    title = models.CharField(max_length=200)
    data = models.JSONField(default=dict)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    users_access = ArrayField(models.CharField(max_length=100), default=list)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    data = models.JSONField(default=dict)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    attempts_allowed = models.IntegerField(default=1)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    users_access = ArrayField(models.CharField(max_length=100), default=list)

    def __str__(self):
        return self.title

