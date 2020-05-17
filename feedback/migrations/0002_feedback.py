# Generated by Django 3.0.1 on 2019-12-28 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.Student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.Subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.Teacher')),
            ],
        ),
    ]
