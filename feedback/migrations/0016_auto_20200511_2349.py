# Generated by Django 3.0.1 on 2020-05-11 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0015_auto_20200327_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.FileField(blank=True, default='feedback/myimages/default.png', null=True, upload_to='feedback/profile_picture'),
        ),
    ]
