from django.db import models

from .querysets import SubscriptionPlanQuerySet, SubscriptionTermQuerySet


class SubscriptionPlanManager(models.Manager):
    def get_queryset(self):
        return SubscriptionPlanQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()



class SubscriptionTermManager(models.Manager):
    def get_queryset(self):
        return SubscriptionTermQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def active_monthly(self, plan_category=None):
        return self.get_queryset().active_monthly(plan_category)

    def active_annual(self, plan_category=None):
        return self.get_queryset().active_annual(plan_category)

    def for_subscription(self, subscription_plan):
        return self.get_queryset().for_subscription(subscription_plan).order_by('price_cents')

    def for_subscription_by_category(self, subscription_plan, plan_category=None):
        return self.get_queryset().for_subscription_by_category(subscription_plan, plan_category).order_by(
            'price_cents')
