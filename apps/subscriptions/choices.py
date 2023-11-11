from django.db import models


class PlanCategories(models.TextChoices):
    DEFAULT = 'default', 'Default'


class IntervalChoices(models.TextChoices):
    MONTHLY = 'monthly', 'Monthly'
    ANNUAL = 'annual', 'Annual'


class StatusChoices(models.TextChoices):
    """
    The status of a subscription order.

    ERROR: The subscription order encountered an error and requires admin intervention.
    PROCESSING: The subscription order has been placed and is being processed.
    PAYMENT_FAILED: The payment failed for the subscription order.
    ACTIVE = The subscription order is active.
    CHECKOUT_CANCELLED = The checkout session was cancelled by the user.
    CANCELLED = The subscription order was cancelled by the user.
    PAST_DUE = If a payment is missed but the service has not yet been suspended, indicating that the subscription
    is at risk of becoming inactive.
    """
    ACTIVE = 'active', 'Active'
    CANCELLED = 'cancelled', 'Cancelled'
    CHECKOUT_CANCELLED = 'checkout_cancelled', 'Checkout cancelled'
    ERROR = 'error', 'Error'
    PAST_DUE = 'past_due', 'Past due'
    PAYMENT_FAILED = 'payment_failed', 'Payment failed'
    PROCESSING = 'processing', 'Processing'
