# Generated by Django 4.2.4 on 2023-10-01 19:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teachers", "0011_remove_quizquestion_question_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quizquestion",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
