from datetime import datetime

import stripe
from django.utils import timezone

from .choices import StatusChoices


# def verify_stripe_subscription(subscription):
#     # Checks the stripe API to see if the subscription is active and updates the local database
#
#     # Get the stripe data via the API
#     stripe_subscription_data = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
#
#     # Update the local database
#     subscription.current_period_start_date = datetime.fromtimestamp(stripe_subscription_data.current_period_start)
#     subscription.current_period_end_date = datetime.fromtimestamp(stripe_subscription_data.current_period_end)
#
#     # Check to see if the subscription has ended
#     if stripe_subscription_data.ended_at:
#         subscription.is_active = False
#         subscription.date_cancelled = datetime.fromtimestamp(stripe_subscription_data.ended_at)
#         subscription.status = StatusChoices.CANCELLED
#
#     if stripe_subscription_data.cancel_at_period_end:
#         logging.debug('CANCELING SOON!')
#         subscription.date_cancelled = datetime.fromtimestamp(stripe_subscription_data.canceled_at)
#         subscription.status = StatusChoices.CANCELLED


class SubscriptionService:
    @staticmethod
    def verify_stripe_subscription(subscription):
        """
        Verifies the status of a Stripe subscription and updates the subscription instance.
        """
        stripe_subscription_data = stripe.Subscription.retrieve(subscription.stripe_subscription_id)

        # Convert the timestamps to a native datetime object
        subscription.current_period_start_date = timezone.make_aware(
            datetime.fromtimestamp(stripe_subscription_data.current_period_start)
        )
        subscription.current_period_end_date = timezone.make_aware(
            datetime.fromtimestamp(stripe_subscription_data.current_period_end)
        )

        if stripe_subscription_data.ended_at:
            subscription.is_active = False
            subscription.date_ended = timezone.make_aware(datetime.fromtimestamp(stripe_subscription_data.ended_at))
            subscription.status = StatusChoices.CANCELLED

        if stripe_subscription_data.cancel_at_period_end:
            subscription.date_cancelled = timezone.make_aware(
                datetime.fromtimestamp(stripe_subscription_data.canceled_at))
            subscription.status = StatusChoices.CANCELLED

        subscription.save()
        return subscription
