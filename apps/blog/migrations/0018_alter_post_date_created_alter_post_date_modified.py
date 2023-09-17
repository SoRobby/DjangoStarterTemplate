# Generated by Django 4.2.4 on 2023-09-17 19:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0017_post_featured_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="date_created",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="Server date and time when the item was created modified",
                verbose_name="Date created",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="date_modified",
            field=models.DateTimeField(
                auto_now=True,
                help_text="Server date and time when the item was last modified",
                verbose_name="Date modified",
            ),
        ),
    ]
