# Generated by Django 4.2.4 on 2023-09-28 15:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("teachers", "0005_alter_quiz_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quiz",
            name="questions",
        ),
    ]
