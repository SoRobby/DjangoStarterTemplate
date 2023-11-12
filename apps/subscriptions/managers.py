import stripe
from django.db import models

from config import settings
from .querysets import SubscriptionPlanQuerySet, SubscriptionPeriodQuerySet

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionPlanManager(models.Manager):
    def get_queryset(self):
        return SubscriptionPlanQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def plan_category(self, plan_category):
        return self.get_queryset().plan_category(plan_category)

    def order_by_price_for_category(self, plan_category):
        return self.get_queryset().order_by_price_for_category(plan_category)

    def order_by_price_for_category_and_interval(self, plan_category, interval):
        return self.get_queryset().order_by_price_for_category_and_interval(plan_category, interval)

    def order_by_interval_rank(self):
        return self.get_queryset().order_by_interval_rank()


class SubscriptionPeriodManager(models.Manager):
    def get_queryset(self):
        return SubscriptionPeriodQuerySet(self.model, using=self._db)

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

    def order_by_interval_rank(self):
        return self.get_queryset().order_by_interval_rank()


class SubscriptionOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
