# Generated by Django 4.2.7 on 2023-12-14 10:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support', '0003_alter_issue_issue_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributor',
            name='user',
        ),
        migrations.AddField(
            model_name='contributor',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]