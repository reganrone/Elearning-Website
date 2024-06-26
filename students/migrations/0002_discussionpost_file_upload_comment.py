# Generated by Django 4.2.4 on 2023-09-26 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="discussionpost",
            name="file_upload",
            field=models.FileField(default="", upload_to="uploads/"),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "discussion_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="students.discussionpost",
                    ),
                ),
            ],
        ),
    ]
