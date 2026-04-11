from django.db import migrations


PDF_PATH = 'protected/materials/class-10-thermodynamics.pdf'


def seed_thermodynamics_material(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Chapter = apps.get_model('courses', 'Chapter')
    StudyMaterial = apps.get_model('courses', 'StudyMaterial')

    course, _ = Course.objects.get_or_create(
        title='Class 10 Thermodynamics',
        class_grade=10,
        defaults={
            'description': (
                'Class 10 thermodynamics notes and guided reading material '
                'available in the secure EduSpark viewer.'
            ),
            'subject': 'science',
        },
    )

    chapter, _ = Chapter.objects.get_or_create(
        course=course,
        order=1,
        title='Thermodynamics Reference',
        defaults={
            'description': 'Reference material and reading support for thermodynamics.',
        },
    )

    StudyMaterial.objects.get_or_create(
        course=course,
        chapter=chapter,
        title='Thermodynamics PDF',
        defaults={
            'description': 'Protected Class 10 thermodynamics PDF for in-site reading.',
            'material_type': 'pdf',
            'file': PDF_PATH,
            'requires_login': True,
            'is_download_allowed': False,
            'sort_order': 1,
        },
    )


def remove_thermodynamics_material(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    StudyMaterial = apps.get_model('courses', 'StudyMaterial')

    StudyMaterial.objects.filter(
        title='Thermodynamics PDF',
        file=PDF_PATH,
    ).delete()
    Course.objects.filter(
        title='Class 10 Thermodynamics',
        class_grade=10,
        chapters__isnull=True,
        materials__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_studymaterial'),
    ]

    operations = [
        migrations.RunPython(seed_thermodynamics_material, remove_thermodynamics_material),
    ]
