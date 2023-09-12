# Generated by Django 4.2.4 on 2023-09-12 07:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0015_post_is_deleted"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="primary_author",
        ),
        migrations.AddField(
            model_name="post",
            name="lead_author",
            field=models.ForeignKey(
                default=1,
                help_text="Lead author of the post",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authored_posts_as_lead",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="post",
            name="meta_description",
            field=models.CharField(
                blank=True,
                help_text="Summary of the post. Recommended length is 50-160 characters.",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="meta_keywords",
            field=models.CharField(
                blank=True,
                help_text="Comma-separated keywords. Keywords that describe the post. Recommended                                     number of keywords is 3-8.",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="meta_title",
            field=models.CharField(
                blank=True,
                help_text="Title that will appear in search engines and browser tab. Recommended                                  length is 50-60 characters.",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="release_status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("review", "Review"),
                    ("published", "Published"),
                    ("archived", "Archived"),
                ],
                default="draft",
                help_text="Current status of the post",
                max_length=55,
                verbose_name="Release status",
            ),
        ),
    ]
