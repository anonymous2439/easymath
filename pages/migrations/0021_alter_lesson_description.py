# Generated by Django 4.1.7 on 2023-03-19 12:03

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0020_alter_submittedactivity_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]