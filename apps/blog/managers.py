from django.db import models
from django.apps import apps


class PostManager(models.Manager):
    def get_model(self):
        return apps.get_model('blog', 'Post')

    def published(self):
        return self.filter(status=self.get_model().STATUS.PUBLISHED)

    def in_draft(self):
        return self.filter(status=self.get_model().STATUS.DRAFT)

    def in_review(self):
        return self.filter(status=self.get_model().STATUS.REVIEW)

    def not_published(self):
        return self.exclude(status=self.get_model().STATUS.PUBLISHED)
