# Generated by Django 4.1.7 on 2023-03-19 05:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0019_submittedactivity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submittedactivity',
            options={'verbose_name': 'SubmittedActivity', 'verbose_name_plural': 'SubmittedActivities'},
        ),
        migrations.AlterUniqueTogether(
            name='submittedactivity',
            unique_together={('activity', 'submitted_by')},
        ),
    ]
