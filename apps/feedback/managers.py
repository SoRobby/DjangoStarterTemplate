from django.db import models

from .querysets import FeedbackQuerySet


class FeedbackManager(models.Manager):
    def get_queryset(self):
        return FeedbackQuerySet(self.model, using=self._db)

    def bug_feedback(self):
        return self.get_queryset().bug_feedback()

    def feature_feedback(self):
        return self.get_queryset().feature_feedback()

    def general_feedback(self):
        return self.get_queryset().general_feedback()

    def other_feedback(self):
        return self.get_queryset().other_feedback()

    def processed(self):
        return self.get_queryset().processed()

    def unprocessed(self):
        return self.get_queryset().unprocessed()
