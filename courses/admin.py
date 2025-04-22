from django.contrib import admin
from .models import Course, Lecture, Assignment


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'create_date')
    search_fields = ('title', 'description', 'owner')
    list_filter = ('create_date',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lecture)
admin.site.register(Assignment)
