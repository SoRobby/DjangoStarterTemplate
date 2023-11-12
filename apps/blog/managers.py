from django.apps import apps
from django.db import models

from .querysets import ArticleQuerySet, CommentQuerySet


class ArticleManager(models.Manager):
    def get_model(self):
        return apps.get_model('blog', 'Article')

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def published(self):
        return self.filter(release_status=self.get_model().ReleaseStatus.PUBLISHED, is_deleted=False)

    def in_draft(self):
        return self.filter(release_status=self.get_model().ReleaseStatus.DRAFT, is_deleted=False)

    def in_review(self):
        return self.filter(release_status=self.get_model().ReleaseStatus.REVIEW, is_deleted=False)

    def not_published(self):
        return self.exclude(release_status=self.get_model().ReleaseStatus.PUBLISHED).exclude(is_deleted=True)

    def with_comments_count(self):
        return self.get_queryset().with_comments_count()


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def with_likes_and_dislikes(self):
        return self.get_queryset().with_likes_and_dislikes()


class CommentAdminManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)
