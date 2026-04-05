from django.db import models


class Course(models.Model):
    SUBJECT_CHOICES = [
        ('mathematics', 'Mathematics'),
        ('science', 'Science'),
        ('english', 'English'),
        ('hindi', 'Hindi'),
        ('social_science', 'Social Science'),
        ('computer', 'Computer Science'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='mathematics')
    class_grade = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
