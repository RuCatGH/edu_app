# Generated by Django 5.1.7 on 2025-03-28 19:12

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, size=None)),
                ('metadata', models.JSONField(default=dict)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_courses', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(blank=True, related_name='attended_courses', to=settings.AUTH_USER_MODEL)),
                ('teachers', models.ManyToManyField(blank=True, related_name='taught_courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('data', models.JSONField(default=dict)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('attempts_allowed', models.IntegerField(default=1)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('users_access', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('data', models.JSONField(default=dict)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('users_access', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
