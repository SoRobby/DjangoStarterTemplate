from django.apps import apps
from django.db import models


class PostManager(models.Manager):
    def get_model(self):
        return apps.get_model('blog', 'Post')

    def published(self):
        return self.filter(release_status=self.get_model().ReleaseStatus.PUBLISHED)

    def in_draft(self):
        return self.filter(release_status=self.get_model().ReleaseStatus.DRAFT)

    def in_review(self):
        return self.filter(release_status=self.get_model().ReleaseStatus.REVIEW)

    def not_published(self):
        return self.exclude(release_status=self.get_model().ReleaseStatus.PUBLISHED)

