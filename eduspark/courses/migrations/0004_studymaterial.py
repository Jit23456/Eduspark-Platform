from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_seed_class10_featured_lecture'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('material_type', models.CharField(choices=[('pdf', 'PDF Document')], default='pdf', max_length=20)),
                ('file', models.FileField(upload_to='protected/materials/')),
                ('is_download_allowed', models.BooleanField(default=False)),
                ('requires_login', models.BooleanField(default=True)),
                ('sort_order', models.PositiveSmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='materials', to='courses.chapter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='courses.course')),
            ],
            options={
                'ordering': ['sort_order', 'title'],
            },
        ),
    ]
