from django.contrib import admin
from .models import Course, Lecture, Assignment, Submission

class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('teachers', 'students')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lecture)
admin.site.register(Assignment)
admin.site.register(Submission)