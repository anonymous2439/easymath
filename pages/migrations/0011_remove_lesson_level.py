# Generated by Django 4.1.7 on 2023-02-28 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_level_lesson_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='level',
        ),
    ]
