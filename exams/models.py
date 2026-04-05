from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('weekly', 'Weekly'),
        ('assignment', 'Assignment'),
        ('mock', 'Mock Test'),
    ]

    SUBJECT_CHOICES = [
        ('mathematics', 'Mathematics'),
        ('science', 'Science'),
        ('english', 'English'),
        ('hindi', 'Hindi'),
        ('social_science', 'Social Science'),
        ('computer', 'Computer Science'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='mathematics')
    class_grade = models.PositiveSmallIntegerField(default=1)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, default='weekly')
    duration_minutes = models.PositiveSmallIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Question(models.Model):
    CORRECT_ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveSmallIntegerField(default=1)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=CORRECT_ANSWER_CHOICES, default='A')

    class Meta:
        ordering = ['exam', 'order']

    def __str__(self):
        return f'{self.exam.title} – Q{self.order}'


class ExamAttempt(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    correct_answers = models.PositiveSmallIntegerField(default=0)
    total_questions = models.PositiveSmallIntegerField(default=0)
    percentage = models.PositiveSmallIntegerField(default=0)
    grade = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        if self.total_questions:
            self.percentage = int(self.correct_answers * 100 / self.total_questions)
            if self.percentage >= 90:
                self.grade = 'A'
            elif self.percentage >= 75:
                self.grade = 'B'
            elif self.percentage >= 60:
                self.grade = 'C'
            elif self.percentage >= 40:
                self.grade = 'D'
            else:
                self.grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.exam.title} attempt on {self.created_at.date()}'


class ExamAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, blank=True)

    @property
    def is_correct(self):
        return self.selected_answer == self.question.correct_answer

    def __str__(self):
        return f'{self.question} – {self.selected_answer or "No answer"}'
