from django.contrib import admin
from .models import Question, Attempt


admin.site.register(Question)
admin.site.register(Attempt)
