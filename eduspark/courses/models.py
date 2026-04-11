import os

from django.db import models
from urllib.parse import parse_qs, urlparse


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


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} – {self.title}'


class Video(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    duration_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    @property
    def get_embed_url(self):
        parsed = urlparse(self.youtube_url)
        video_id = None

        if 'youtu.be' in parsed.netloc:
            video_id = parsed.path.lstrip('/')
        elif 'youtube.com' in parsed.netloc:
            query = parse_qs(parsed.query)
            video_id = query.get('v', [None])[0]
            if not video_id and parsed.path.startswith('/embed/'):
                video_id = parsed.path.split('/')[-1]

        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'
        return self.youtube_url


class Assignment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    instructions = models.TextField(blank=True)

    class Meta:
        ordering = ['chapter__order']

    def __str__(self):
        return self.title


class StudyMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('pdf', 'PDF Document'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.SET_NULL,
        related_name='materials',
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES, default='pdf')
    file = models.FileField(upload_to='protected/materials/')
    is_download_allowed = models.BooleanField(default=False)
    requires_login = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return os.path.basename(self.file.name or '')
