import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from .managers import SubscriptionPlanManager, SubscriptionTermManager
from .validators import validate_features_list


# Models
class SubscriptionPlan(BaseModel):
    class PlanCategories(models.TextChoices):
        DEFAULT = 'default', 'Default'

    name = models.CharField(max_length=120, verbose_name='Name', help_text='Name of the subscription plan')

    description = models.TextField(max_length=1000, verbose_name='Description',
                                   help_text='Short description of the subscription plan')

    plan_category = models.CharField(max_length=24, choices=PlanCategories.choices, default=PlanCategories.DEFAULT,
                                     help_text='Allows for multiple subscription plan categories (e.g.,\
                                     analytics plans, advertising plans, etc.)')

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

    objects = SubscriptionPlanManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Subscription plan'
        verbose_name_plural = 'Subscription plans'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.is_active:
            self.subscription_terms.update(is_active=False)

    @property
    def features(self):
        if isinstance(self.features_list, list):
            return self.features_list
        elif not isinstance(self.features_list, list):
            logging.error('SubscriptionPlan.features: features_list is not a list')
            raise TypeError('SubscriptionPlan.features: features_list is not a list')
        else:
            return []

    @property
    def monthly_term(self):
        """The monthly term for this subscription plan."""
        return self.subscription_terms.filter(interval=SubscriptionTerm.IntervalChoices.MONTHLY).first()

    @property
    def annual_term(self):
        """The monthly term for this subscription plan."""
        return self.subscription_terms.filter(interval=SubscriptionTerm.IntervalChoices.ANNUAL).first()


class SubscriptionTerm(BaseModel):
    class IntervalChoices(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        ANNUAL = 'annual', 'Annual'

    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name='Subscription plan',
                                          related_name='subscription_terms',
                                          help_text='Subscription plan that this term belongs to')

    price_cents = models.PositiveIntegerField(blank=True, null=True, verbose_name='Price cents',
                                              help_text='Price in cents (e.g. 1000 = $10.00)')

    stripe_price_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Stripe price ID',
                                       help_text='Stripe price API ID (e.g. "price_1KVqZYGH7IAkWYyXOExqnpAw")')

    interval = models.CharField(max_length=24, choices=IntervalChoices.choices, default=IntervalChoices.MONTHLY,
                                help_text='Billing interval for this term')

    is_active = models.BooleanField(default=True, help_text='If true, this subscription term is available for purchase')

    admin_notes = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Admin notes',
                                   help_text='Notes for the staff and admins, notes are not shown to the users')

    objects = SubscriptionTermManager()

    class Meta:
        ordering = ('price_cents',)
        verbose_name = 'Subscription term'
        verbose_name_plural = 'Subscription terms'
        constraints = [
            models.UniqueConstraint(fields=['subscription_plan', 'interval'], name='unique_subscription_plan_interval')
        ]

    def __str__(self):
        return f'{self.subscription_plan.name} ({self.get_interval_display()})'

    def clean(self):
        # Call the superclass's clean method to ensure any other validation logic is preserved
        super().clean()

        # Check if the subscription_plan is_active field is False
        if self.subscription_plan.is_active is False and self.is_active is True:
            raise ValidationError({'subscription_plan': 'The related SubscriptionPlan must be active, the field\
            is_active is currently set to False'})

    @property
    def price_dollars(self):
        """The price in dollars. Converts cents to a dollar value."""
        result = round(self.price_cents / 100.0, 2)
        return "{:.2f}".format(result)


class SubscriptionOrder(BaseModel):
    class PurchaseStatusChoices(models.TextChoices):
        CHECKOUT_CANCELLED = 'checkout_cancelled', 'Checkout cancelled'
        SUBSCRIPTION_CANCELLED = 'subscription_cancelled', 'Subscription cancelled'
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        PAYMENT_FAILED = 'payment_failed', 'Payment failed'
        REFUNDED = 'refunded', 'Refunded'

    purchaser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='subscription_orders',
                                  help_text='The user who purchased the subscription')

    subscription_term = models.ForeignKey(SubscriptionTerm, on_delete=models.SET_NULL, null=True,
                                          related_name='subscription_orders',
                                          help_text='The subscription term that was purchased')

    purchase_status = models.CharField(max_length=50, choices=PurchaseStatusChoices.choices,
                                       help_text='Purchase status')

    auto_renew = models.BooleanField(default=True,
                                     help_text='If true, the subscription will automatically renew at the end of the\
                                     term')

    is_active = models.BooleanField(default=True, help_text='If true, this subscription order is active')

    date_start = models.DateTimeField(auto_now_add=True, help_text='Date when the subscription period started')

    date_end = models.DateTimeField(blank=True, null=True, help_text='Date when the subscription period will end')

    date_renewal = models.DateTimeField(blank=True, null=True, help_text='Date the subscription will renew')

    date_cancelled = models.DateTimeField(blank=True, null=True, help_text='Date the subscription was cancelled')

    date_refunded = models.DateTimeField(blank=True, null=True, help_text='Date the subscription was refunded')

    date_changed_plan = models.DateTimeField(blank=True, null=True, help_text='Date the subscription plan was changed')

    date_payment_failed = models.DateTimeField(blank=True, null=True, help_text='Date the payment failed')

    stripe_checkout_session_id = models.CharField(max_length=255, blank=True, null=True,
                                                  verbose_name='Stripe checkout session ID',
                                                  help_text='Stripe checkout session ID')

    stripe_product_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Stripe product ID',
                                         help_text='Stripe product ID at the time of the order')

    stripe_price_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Stripe price ID',
                                       help_text='Stripe price ID at the time of the order')

    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True,
                                              verbose_name='Stripe subscription ID',
                                              help_text='Stripe subscription ID at the time of the order')

    staff_notes = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Staff notes',
                                   help_text='Notes for the staff and admins, notes are not shown to the users')

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'Subscription order'
        verbose_name_plural = 'Subscription orders'

    def __str__(self):
        return f'{self.pk} - {self.purchaser.username}'


    def checkout_cancelled(self):
        """Set the status to cancelled and set the date_cancelled field to now."""
        self.purchase_status = self.PurchaseStatusChoices.CHECKOUT_CANCELLED
        self.is_active = False
        self.save()




