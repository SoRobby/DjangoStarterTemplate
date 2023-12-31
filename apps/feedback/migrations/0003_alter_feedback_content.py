# Generated by Django 4.2.5 on 2023-10-24 20:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0002_alter_feedback_options_alter_feedback_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="content",
            field=models.TextField(
                default=django.utils.timezone.now,
                help_text="Content of the feedback",
                max_length=3000,
                verbose_name="Content",
            ),
            preserve_default=False,
        ),
    ]
