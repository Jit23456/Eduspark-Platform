from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'class_grade', 'created_at')
    list_filter = ('subject', 'class_grade')
    search_fields = ('title', 'description')
