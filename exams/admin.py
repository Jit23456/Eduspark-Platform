from django.contrib import admin

from .models import Exam, ExamAnswer, ExamAttempt, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('order', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')


class ExamAnswerInline(admin.TabularInline):
    model = ExamAnswer
    extra = 0
    readonly_fields = ('question', 'selected_answer')
    can_delete = False


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'class_grade', 'exam_type', 'duration_minutes')
    list_filter = ('subject', 'class_grade', 'exam_type')
    search_fields = ('title',)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'order', 'question_text')
    list_filter = ('exam',)
    search_fields = ('question_text',)


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('exam', 'user', 'created_at', 'correct_answers', 'total_questions', 'percentage', 'grade')
    list_filter = ('exam', 'grade')
    search_fields = ('exam__title',)
    readonly_fields = ('percentage', 'grade')
    inlines = [ExamAnswerInline]
