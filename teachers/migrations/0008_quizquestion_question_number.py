# Generated by Django 4.2.4 on 2023-10-01 00:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teachers", "0007_lesson"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizquestion",
            name="question_number",
            field=models.PositiveIntegerField(default=None),
        ),
    ]
