from django.db import migrations


YOUTUBE_URL = "https://youtu.be/Z_e0ToEM8XU?si=y5-ExEsTL66aBNOo"


def seed_class10_featured_lecture(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    Chapter = apps.get_model("courses", "Chapter")
    Video = apps.get_model("courses", "Video")

    course, _ = Course.objects.get_or_create(
        title="Class 10 Video Lectures",
        class_grade=10,
        defaults={
            "description": (
                "A Class 10 course with curated video lectures that can be "
                "watched from anywhere."
            ),
            "subject": "computer",
        },
    )

    chapter, _ = Chapter.objects.get_or_create(
        course=course,
        order=1,
        title="Featured Lecture",
        defaults={
            "description": "Featured lecture content for Class 10 students.",
        },
    )

    Video.objects.get_or_create(
        chapter=chapter,
        youtube_url=YOUTUBE_URL,
        defaults={
            "title": "Class 10 Featured Lecture",
            "duration_minutes": 15,
            "description": (
                "Featured YouTube lecture added for Class 10 learners. "
                "Update the title or duration later if you want the exact "
                "lesson details shown in the app."
            ),
        },
    )


def remove_class10_featured_lecture(apps, schema_editor):
    Video = apps.get_model("courses", "Video")
    Chapter = apps.get_model("courses", "Chapter")
    Course = apps.get_model("courses", "Course")

    Video.objects.filter(youtube_url=YOUTUBE_URL).delete()
    Chapter.objects.filter(
        course__title="Class 10 Video Lectures",
        course__class_grade=10,
        title="Featured Lecture",
    ).delete()
    Course.objects.filter(
        title="Class 10 Video Lectures",
        class_grade=10,
        chapters__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_chapter_assignment_video"),
    ]

    operations = [
        migrations.RunPython(
            seed_class10_featured_lecture,
            remove_class10_featured_lecture,
        ),
    ]
