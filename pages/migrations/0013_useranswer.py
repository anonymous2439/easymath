# Generated by Django 4.1.7 on 2023-02-28 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0012_lesson_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
