from django.apps import apps
from django.db import models


class ArticleManager(models.Manager):
    def get_model(self):
        return apps.get_model('blog', 'Article')

    def published(self):
        return self.filter(release_status=self.get_model().ReleaseStatus.PUBLISHED, is_deleted=False)

    def in_draft(self):
        return self.filter(release_status=self.get_model().ReleaseStatus.DRAFT, is_deleted=False)

    def in_review(self):
        return self.filter(release_status=self.get_model().ReleaseStatus.REVIEW, is_deleted=False)

    def not_published(self):
        return self.exclude(release_status=self.get_model().ReleaseStatus.PUBLISHED).exclude(is_deleted=True)
