import logging
from datetime import datetime

import stripe
from django.db import models

from config import settings
from .choices import StatusChoices
from .querysets import SubscriptionPlanQuerySet, SubscriptionPeriodQuerySet

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionPlanManager(models.Manager):
    def get_queryset(self):
        return SubscriptionPlanQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


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


class SubscriptionOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


