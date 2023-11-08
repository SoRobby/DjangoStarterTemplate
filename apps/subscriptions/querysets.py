from django.db import models


class SubscriptionPlanQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class SubscriptionPeriodQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def active_monthly(self, plan_category=None):
        queryset = self.active().filter(interval=self.model.IntervalChoices.MONTHLY)
        if plan_category:
            print(plan_category)
            queryset = queryset.filter(subscription_plan__plan_category=plan_category)
        return queryset.order_by('price_cents')

    def active_annual(self, plan_category=None):
        queryset = self.active().filter(interval=self.model.IntervalChoices.ANNUAL)
        if plan_category:
            queryset = queryset.filter(subscription_plan__plan_category=plan_category)
        return queryset.order_by('price_cents')

    def for_subscription(self, subscription):
        return self.filter(subscription_plan=subscription)

    def for_subscription_by_category(self, subscription_plan, plan_category=None):
        queryset = self.active().filter(subscription_plan=subscription_plan)
        if plan_category and subscription_plan.plan_category == plan_category:
            queryset = queryset.filter(subscription_plan__plan_category=plan_category)

        return queryset.order_by('price_cents')
