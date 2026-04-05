from django.contrib import admin

from .models import Assignment, Chapter, Course, Video


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 1
    fields = ('title', 'order', 'description')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'class_grade', 'created_at')
    list_filter = ('subject', 'class_grade')
    search_fields = ('title', 'description')
    inlines = [ChapterInline]


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = ('title', 'youtube_url', 'duration_minutes', 'description')


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1
    fields = ('title', 'due_date', 'instructions')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course', 'course__subject', 'course__class_grade')
    ordering = ('course', 'order')
    search_fields = ('title', 'description', 'course__title')
    inlines = [VideoInline, AssignmentInline]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'duration_minutes')
    list_filter = ('chapter__course', 'chapter__course__subject', 'chapter__course__class_grade')
    search_fields = ('title', 'youtube_url', 'description')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'due_date')
    list_filter = ('chapter__course', 'due_date')
    search_fields = ('title', 'instructions', 'chapter__title')
