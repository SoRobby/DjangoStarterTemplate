# Generated by Django 4.2.4 on 2023-09-18 04:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0021_post_authors_alter_post_date_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="meta_description",
            field=models.CharField(
                blank=True,
                help_text="Summary of the post. Recommended length is 50-160 characters",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="meta_keywords",
            field=models.CharField(
                blank=True,
                help_text="Comma-separated keywords. Keywords that describe the post. Recommended                                     number of keywords is 3-8",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="meta_title",
            field=models.CharField(
                blank=True,
                help_text="Title that will appear in search engines and browser tab. Recommended                                  length is 50-60 characters",
                max_length=200,
                null=True,
            ),
        ),
    ]