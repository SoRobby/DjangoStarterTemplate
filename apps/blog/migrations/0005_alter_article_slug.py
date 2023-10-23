# Generated by Django 4.2.4 on 2023-10-23 02:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_article_number_of_revisions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="The URL slug based on the article title, slug fields should be 50 characters or                            less",
                max_length=200,
                null=True,
                unique=True,
                verbose_name="Slug",
            ),
        ),
    ]