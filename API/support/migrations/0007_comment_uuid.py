# Generated by Django 4.2.7 on 2023-12-16 12:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0006_contributor_uuid_issue_uuid_project_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
