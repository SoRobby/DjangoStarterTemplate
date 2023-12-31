# Generated by Django 4.2.4 on 2023-10-23 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_alter_article_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="article",
            field=models.ForeignKey(
                help_text="The article that the comment is related to",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comment",
                to="blog.article",
                verbose_name="Article",
            ),
        ),
    ]
