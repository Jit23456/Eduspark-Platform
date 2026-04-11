import shutil
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Course, StudyMaterial


MEDIA_ROOT = Path(__file__).resolve().parents[2] / 'test_media'
MEDIA_ROOT.mkdir(exist_ok=True)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class StudyMaterialSecurityTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.course = Course.objects.create(
            title='Class 10 Thermodynamics',
            description='Secure notes',
            subject='science',
            class_grade=10,
        )
        self.user = User.objects.create_user(username='student1', password='strong-pass-123')
        self.material = StudyMaterial.objects.create(
            course=self.course,
            title='Thermodynamics PDF',
            file=SimpleUploadedFile(
                'thermodynamics.pdf',
                b'%PDF-1.4 test pdf bytes',
                content_type='application/pdf',
            ),
        )

    def test_material_stream_requires_login(self):
        response = self.client.get(reverse('material_stream', args=[self.material.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_material_stream_sets_inline_security_headers(self):
        self.client.login(username='student1', password='strong-pass-123')
        response = self.client.get(reverse('material_stream', args=[self.material.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('inline;', response['Content-Disposition'])
        self.assertIn('no-store', response['Cache-Control'])
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')

    def test_mira_endpoint_guides_to_login(self):
        response = self.client.get(reverse('mira_assistant'), {'q': 'How do I use google login?'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Google')
