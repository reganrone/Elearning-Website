# Generated by Django 4.2.4 on 2023-10-11 00:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("teachers", "0016_alter_classroom_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
