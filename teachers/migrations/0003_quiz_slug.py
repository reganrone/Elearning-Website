# Generated by Django 4.2.4 on 2023-09-27 21:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("teachers", "0002_quiz_grade"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="slug",
            field=models.SlugField(default=django.utils.timezone.now),
        ),
    ]