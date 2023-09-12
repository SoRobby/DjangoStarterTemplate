from django.db import models
from django.apps import apps


class PostManager(models.Manager):
    def get_model(self):
        return apps.get_model('blog', 'Post')

    def published(self):
        return self.filter(release_status=self.get_model().RELEASE_STATUS.PUBLISHED)

    def in_draft(self):
        return self.filter(release_status=self.get_model().RELEASE_STATUS.DRAFT)

    def in_review(self):
        return self.filter(release_status=self.get_model().RELEASE_STATUS.REVIEW)

    def not_published(self):
        return self.exclude(release_status=self.get_model().RELEASE_STATUS.PUBLISHED)
