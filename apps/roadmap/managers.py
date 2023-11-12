from django.db import models

from .querysets import FeatureQuerySet


class FeatureManager(models.Manager):
    def get_queryset(self):
        return FeatureQuerySet(self.model, using=self._db)

    def in_progress(self):
        return self.get_queryset().in_progress()

    def planned(self):
        return self.get_queryset().planned()

    def archived(self):
        return self.get_queryset().archived()

    def released_by_month(self):
        return self.get_queryset().released_by_month()
