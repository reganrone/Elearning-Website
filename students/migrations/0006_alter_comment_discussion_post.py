# Generated by Django 4.2.4 on 2023-09-28 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0005_alter_discussionpost_file_upload"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="discussion_post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="students.discussionpost",
            ),
        ),
    ]