from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncMonth


class FeatureQuerySet(models.QuerySet):
    def planned(self):
        return self.filter(release_status=self.model.ReleaseStatus.PLANNED)

    def in_progress(self):
        return self.filter(release_status=self.model.ReleaseStatus.IN_PROGRESS)

    def released(self):
        return self.filter(release_status=self.model.ReleaseStatus.RELEASED)

    def archived(self):
        return self.filter(release_status=self.model.ReleaseStatus.ARCHIVED)

    def released_by_month(self):
        return (
            self.filter(release_status=self.model.ReleaseStatus.RELEASED)
            .annotate(month=TruncMonth('date_released'))
            .values('month')
            .annotate(feature_count=Count('id'))
            .filter(feature_count__gt=0)
            .order_by('-month')
        )
