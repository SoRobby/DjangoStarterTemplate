from django.db import models
from django.db.models import Case, When, IntegerField, Min

from .choices import IntervalChoices


class SubscriptionPlanQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def plan_category(self, plan_category):
        return self.filter(plan_category=plan_category)

    def order_by_price_for_category(self, plan_category):
        queryset = self.filter(
            plan_category=plan_category,
        ).annotate(
            price_cents=models.Min('subscription_terms__price_cents')
        ).order_by('price_cents')

        return queryset

    def order_by_price_for_category_and_interval(self, plan_category, interval):
        queryset = self.filter(
            plan_category=plan_category,
            subscription_terms__interval=interval
        ).annotate(
            price_cents=models.Min('subscription_terms__price_cents')
        ).order_by('price_cents')

        return queryset

    def ordered_by_price_for_category_and_interval(self, plan_category, interval):
        return self.filter(
            plan_category=plan_category,
            subscription_terms__interval=interval,
            subscription_terms__is_active=True
        ).annotate(
            lowest_price=models.Min('subscription_terms__price_cents')
        ).order_by('price_cents')

    def order_by_interval_rank(self):
        interval_rank_ordering = Case(
            *[When(subscription_terms__interval=choice.value, then=choice.rank) for choice in IntervalChoices],
            output_field=IntegerField()
        )

        return self.active().annotate(
            lowest_interval_rank=Min(interval_rank_ordering)
        ).order_by('lowest_interval_rank')

    # def order_by_interval_rank(self):
    #     ordering = Case(
    #         *[When(interval=choice.value, then=choice.rank) for choice in IntervalChoices],
    #         output_field=IntegerField()
    #     )
    #
    #     queryset = self.annotate(interval_rank=ordering).order_by('interval_rank')
    #     return queryset

    # custom_ordering = Case(
    #     When(interval=IntervalChoices.MONTHLY, then=1),
    #     When(interval=IntervalChoices.ANNUAL, then=2),
    #     default=5,
    #     output_field=IntegerField()
    # )
    # return self.get_queryset().annotate(custom_order=custom_ordering).order_by('custom_order')

    # def order_by_custom_interval(self):
    #     custom_ordering = Case(
    #         When(interval=IntervalChoices.WEEKLY, then=1),
    #         When(interval=IntervalChoices.MONTHLY, then=2),
    #         When(interval=IntervalChoices.QUARTERLY, then=3),
    #         When(interval=IntervalChoices.ANNUAL, then=4),
    #         default=5,
    #         output_field=IntegerField()
    #     )
    #     return self.get_queryset().annotate(custom_order=custom_ordering).order_by('custom_order')


class SubscriptionPeriodQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def active_monthly(self, plan_category=None):
        queryset = self.active().filter(interval=IntervalChoices.MONTHLY)
        if plan_category:
            print(plan_category)
            queryset = queryset.filter(subscription_plan__plan_category=plan_category)
        return queryset.order_by('price_cents')

    def active_annual(self, plan_category=None):
        queryset = self.active().filter(interval=IntervalChoices.ANNUAL)
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

    def order_by_interval_rank(self):
        interval_rank_ordering = Case(
            *[When(interval=choice.value, then=choice.rank) for choice in IntervalChoices],
            output_field=IntegerField()
        )
        return self.annotate(interval_rank=interval_rank_ordering).order_by('interval_rank')
