# Generated by Django 4.1.7 on 2023-04-27 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_role_delete_userrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
    ]
