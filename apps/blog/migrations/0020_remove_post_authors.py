# Generated by Django 4.2.4 on 2023-09-17 19:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0019_alter_post_date_created_alter_post_date_deleted_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="authors",
        ),
    ]
