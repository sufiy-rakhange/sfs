# Generated by Django 3.0.1 on 2020-03-27 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0014_teacher_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.FileField(blank=True, upload_to='feedback/profile_picture'),
        ),
    ]
