# Generated by Django 4.2.4 on 2023-10-19 23:08

import apps.blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={
                "ordering": ["-date_published", "-date_created"],
                "verbose_name": "Article",
                "verbose_name_plural": "Articles",
            },
        ),
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ["-date_created"],
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
        ),
        migrations.RemoveField(
            model_name="comment",
            name="downvotes",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="upvotes",
        ),
        migrations.AddField(
            model_name="comment",
            name="dislikes",
            field=models.ManyToManyField(
                blank=True,
                help_text="Users who have disliked this comment",
                related_name="comment_dislikes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Dislikes",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="likes",
            field=models.ManyToManyField(
                blank=True,
                help_text="Users who have liked this comment",
                related_name="comment_likes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Likes",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="created_by",
            field=models.ForeignKey(
                help_text="User who created the article",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_articles",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created by",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="deleted_by",
            field=models.ForeignKey(
                blank=True,
                help_text="User who deleted the article",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="deleted_articles",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Deleted by",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="featured_image",
            field=models.ImageField(
                blank=True,
                help_text="Featured image of the article",
                null=True,
                upload_to=apps.blog.models.upload_to_featured_images,
                verbose_name="Featured thumbnail",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="featured_image_raw",
            field=models.ImageField(
                blank=True,
                help_text="Original unedited image of the article",
                null=True,
                upload_to=apps.blog.models.upload_to_featured_images,
                verbose_name="Featured thumbnail raw",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="featured_image_thumbnail",
            field=models.ImageField(
                blank=True,
                help_text="Featured image thumbnail of the article",
                null=True,
                upload_to=apps.blog.models.upload_to_featured_images,
                verbose_name="Featured thumbnail",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="lead_author",
            field=models.ForeignKey(
                help_text="Lead author of the article",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authored_articles_as_lead",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Lead author",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="meta_keywords",
            field=models.CharField(
                blank=True,
                help_text="Comma-separated keywords. Keywords that describe the article.                                     Recommended number of keywords is 3-8",
                max_length=200,
                null=True,
                verbose_name="Meta keywords",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="meta_title",
            field=models.CharField(
                blank=True,
                help_text="Title that will appear in search engines and browser tab. Recommended                                  length is 50-60 characters",
                max_length=200,
                null=True,
                verbose_name="Meta title",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="modified_by",
            field=models.ForeignKey(
                help_text="User who last modified the article",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="modified_articles",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Modified by",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="The URL slug based on the article title, slug fields should be 50 characters or                            less",
                max_length=200,
                null=True,
                unique=True,
                verbose_name="Lead author",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="article",
            field=models.ForeignKey(
                help_text="The article that the comment is related to",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="article_comment",
                to="blog.article",
                verbose_name="Article",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="parent_comment",
            field=models.ForeignKey(
                blank=True,
                help_text="The parent comment that this comment replied to",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="child_comments",
                to="blog.comment",
                verbose_name="Parent comment",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                help_text="User that made the comment",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_comment",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]