import logging

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel


# Model validators
def validate_features_list(value):
    if not isinstance(value, list):
        raise ValidationError('This field must be a list')


# Models
class SubscriptionPlan(BaseModel):
    name = models.CharField(max_length=120, verbose_name='Name', help_text='Name of the subscription plan')

    description = models.TextField(max_length=1000, verbose_name='Description',
                                   help_text='Short description of the subscription plan')

    stripe_product_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Stripe product ID',
                                         help_text='Stripe product API ID (e.g. "prod_1KVqZYGH7I")')

    is_plan_showcased = models.BooleanField(default=False,
                                            help_text='If true, this subscription plan is showcased on the pricing\
                                            page')

    is_active = models.BooleanField(default=True, help_text='If true, this plan is available for purchase')

    features_list = models.JSONField(default=list, blank=True, null=True, verbose_name='Features list',
                                     help_text='Features list, features are separated by comma (e.g.,\
                                          ["5 products", "Basic analytics", ...])',
                                     validators=[validate_features_list])

    json_data = models.JSONField(default=dict, blank=True, null=True, verbose_name='JSON data', help_text='JSON data')

    admin_notes = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Admin notes',
                                   help_text='Notes for the staff and admins, notes are not shown to the users')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Subscription plan'
        verbose_name_plural = 'Subscription plans'

    def __str__(self):
        return self.name

    @property
    def features(self):
        if isinstance(self.features_list, list):
            return self.features_list
        elif not isinstance(self.features_list, list):
            logging.error('SubscriptionPlan.features: features_list is not a list')
            raise TypeError('SubscriptionPlan.features: features_list is not a list')
        else:
            return []


class SubscriptionTerm(BaseModel):
    class IntervalChoices(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        ANNUAL = 'annual', 'Annual'

    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name='Subscription plan',
                                          related_name='subscription_terms',
                                          help_text='Subscription plan that this term belongs to')

    price_cents = models.IntegerField(blank=True, null=True, verbose_name='Price cents',
                                      help_text='Price in cents (e.g. 1000 = $10.00)')

    stripe_price_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Stripe price ID',
                                       help_text='Stripe price API ID (e.g. "price_1KVqZYGH7IAkWYyXOExqnpAw")')

    interval = models.CharField(max_length=24, choices=IntervalChoices.choices, default=IntervalChoices.MONTHLY,
                                help_text='Billing interval for this term')

    is_active = models.BooleanField(default=True, help_text='If true, this subscription term is available for purchase')

    admin_notes = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Admin notes',
                                   help_text='Notes for the staff and admins, notes are not shown to the users')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Subscription term'
        verbose_name_plural = 'Subscription terms'
        constraints = [
            models.UniqueConstraint(fields=['subscription_plan', 'interval'], name='unique_subscription_plan_interval')
        ]

    def __str__(self):
        return f'{self.subscription_plan.name} ({self.get_interval_display()})'

    @property
    def price_dollars(self):
        result = round(self.price_cents / 100.0, 2)
        return "{:.2f}".format(result)

    def print_hello(self, *args, **kwargs):
        """
        This is a test method that is used to test the SubscriptionTerm model

        INPUTS:
        - args: tuple
        """
        print('hello')
