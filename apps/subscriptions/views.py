import logging
import urllib
import urllib.parse
from datetime import datetime

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.core.utils import send_error_notification, send_success_notification
from .models import SubscriptionPlan, SubscriptionPeriod, SubscriptionOrder
from .choices import PlanCategories, IntervalChoices, StatusChoices
from .services import SubscriptionService

# Set the api key
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def subscription_plans(request):
    context = {}
    plan_category = PlanCategories.DEFAULT

    subscription_plans = SubscriptionPlan.objects.active().filter(plan_category=plan_category)
    subscription_terms = SubscriptionPeriod.objects.active().filter(subscription_plan__in=subscription_plans).order_by(
        'price_cents')

    monthly_plans = SubscriptionPeriod.objects.active_monthly(plan_category=plan_category)
    annual_plans = SubscriptionPeriod.objects.active_annual(plan_category=plan_category)

    context['monthly_plans'] = monthly_plans
    context['annual_plans'] = annual_plans
    context['subscription_plans'] = subscription_plans

    logging.debug(f'monthly_plans = {monthly_plans}')
    logging.debug(f'annual_plans = {annual_plans}')
    logging.debug(f'subscription_plans = {subscription_plans}')

    # Testing

    # Get the users active subscription
    user_subscription = SubscriptionOrder.objects.filter(purchaser=request.user,
                                                         is_active=True).order_by('-date_created')

    if user_subscription:
        user_subscription = user_subscription.first()

        context['user_subscription'] = user_subscription

        print(f'active_sub = {user_subscription}')

        stripe_subscription_id = user_subscription.stripe_subscription_id
        try:
            SubscriptionService.verify_stripe_subscription(user_subscription)
            # return subscription.status  # possible values are 'active', 'past_due', 'canceled', and others
        except stripe.error.StripeError as e:
            logging.error('Error retrieving subscription')
            logging.error(e)
            # Handle error
            pass


    user_subscription = SubscriptionOrder.objects.filter(purchaser=request.user,
                                                         is_active=True).order_by('-date_created')
    if user_subscription:
        context['user_subscription'] = user_subscription

    # annual_plans = SubscriptionTerm.objects.active().annual(category_type)

    return render(request, 'subscriptions/plans.html', context)


# def subscription_checkout(request, term_uuid):
#     context = {}
#
#     # Get the subscription Term or 404
#     term = SubscriptionTerm.objects.get_object_or_404(uuid=term_uuid)


class CheckoutSessionCreateView(View):
    def post(self, request, *args, **kwargs):
        logging.debug('CreateCheckoutSessionView.post()')

        domain_partial_url = request.build_absolute_uri('/')[:-1]
        logging.debug(f'domain_partial_url = {domain_partial_url}')

        # Get the subscription information
        term_uuid = kwargs.get('term_uuid')
        subscription_period = get_object_or_404(SubscriptionPeriod, uuid=term_uuid)
        logging.debug(f'Selected period = {subscription_period}')

        # User purchasing
        purchaser = request.user

        try:
            order = SubscriptionOrder.objects.create(
                purchaser=purchaser,
                subscription_period=subscription_period,
                status=SubscriptionOrder.StatusChoices.PROCESSING,
            )

            # Set the stripe variables
            success_partial_url = reverse('subscriptions:subscription-checkout-success', kwargs={
                'term_uuid': term_uuid,
                'order_uuid': order.uuid
            })
            success_url = urllib.parse.urljoin(domain_partial_url, success_partial_url)

            # If the user cancels the payment, the cancel url will retrieve the order by uuid and set the status to
            # cancelled
            cancel_partial_url = reverse('subscriptions:subscription-checkout-cancel', kwargs={
                'term_uuid': term_uuid,
                'order_uuid': order.uuid
            })
            cancel_url = urllib.parse.urljoin(domain_partial_url, cancel_partial_url)

            # Format the Stripe payment request
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': subscription_period.stripe_price_id,  # e.g. price_1KVqZYGH7IAkWYyXOExqnpAw
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url + '?session_id={CHECKOUT_SESSION_ID}',
                customer_email=purchaser.email,
                metadata={
                    'order_uuid': str(order.uuid),
                }
            )

            logging.debug('SubscriptionOrder created')
            return HttpResponseRedirect(checkout_session.url)

        except:
            logging.error('Error creating SubscriptionOrder')
            send_error_notification(request, title='Error occurred during order setup',
                                    message='An error occurred during the order setup and could not be completed,\
                                    please try again later')
            raise

        # YOUR_DOMAIN = "http://127.0.0.1:8000/"
        #
        # term_uuid = kwargs.get('term_id')
        # term = get_object_or_404(SubscriptionTerm, uuid=term_uuid)
        # checkout_session = stripe.checkout.Session.create(
        #     payment_method_types=['card'],
        #     line_items=[{
        #         'price': term.stripe_price_id,
        #         'quantity': 1,
        #     }],
        #     mode='subscription',
        #     success_url=YOUR_DOMAIN + '/success/',
        #     cancel_url=YOUR_DOMAIN + '/cancel/',
        # )
        # return JsonResponse({
        #     'id': checkout_session.id
        # })


class CheckoutSessionCancelView(View):
    def get(self, request, *args, **kwargs):
        send_error_notification(request, title='Payment cancelled', message='Payment cancelled by user')

        # Get the order_uuid
        order_uuid = kwargs.get('order_uuid')
        order = get_object_or_404(SubscriptionOrder, uuid=order_uuid)

        # Set the order status to cancelled
        order.checkout_cancelled()

        return redirect('subscriptions:subscription-plans')


class CheckoutSessionSuccessView(View):
    def get(self, request, *args, **kwargs):
        # Get the order_uuid
        order_uuid = kwargs.get('order_uuid')
        order = get_object_or_404(SubscriptionOrder, uuid=order_uuid)

        # Set the checkout as error, but then update if the data is processed successfully from stripe.
        # In rare cases, the processed stripe data may error, even if the payment was successful, if this happens
        # an admin will need to manually update the order status.
        order.checkout_error()

        # Retrieve the stripe session
        stripe_session_id = request.GET.get('session_id')

        # Get the stripe session
        stripe_session = stripe.checkout.Session.retrieve(stripe_session_id)

        stripe_subscription_id = stripe_session.subscription

        line_items = stripe.checkout.Session.list_line_items(stripe_session_id)

        if len(line_items) == 0:
            send_error_notification(request, title='Payment failed',
                                    message='Payment failed, please try again later')
            return redirect('subscriptions:subscription-plans')

        elif len(line_items) == 1:
            stripe_product_id = line_items.data[0].price.product
            stripe_price_id = line_items.data[0].price.id

            order.set_stripe_data(
                stripe_checkout_session_id=stripe_session_id,
                stripe_product_id=stripe_product_id,
                stripe_price_id=stripe_price_id,
                stripe_subscription_id=stripe_subscription_id,
            )
            order.checkout_success()

            send_success_notification(request, title='Payment successful',
                                      message='Your account has been successfully upgraded')

        # logging.debug(f'stripe_session = {stripe_session}')
        # logging.debug(f'line_items = {line_items}')
        # for item in line_items:
        #     print(f'item = {item}')

        # Set the order status to paid

        send_success_notification(request, title='Payment successful',
                                  message='Your account has been successfully upgraded')

        return redirect('subscriptions:subscription-plans')


@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
        # Payment was successful
        pass  # TODO: Implement your logic here
    elif event['type'] == 'invoice.payment_failed':
        # Payment failed
        pass  # TODO: Implement your logic here
    elif event['type'] == 'customer.subscription.deleted':
        # Subscription was cancelled
        pass  # TODO: Implement your logic here

    return HttpResponse(status=200)


@method_decorator(login_required, name='dispatch')
class CancelSubscriptionView(View):
    def post(self, request, *args, **kwargs):
        subscription_uuid = kwargs.get('subscription_uuid')
        user_subscription = SubscriptionOrder.objects.get(uuid=subscription_uuid)

        # Make sure the user owns the subscription
        if user_subscription.purchaser == request.user:
            try:
                # Attempt to retrieve the subscription from Stripe
                subscription = stripe.Subscription.retrieve(user_subscription.stripe_subscription_id)

                if subscription.status == 'active':
                    subscription.cancel_at_period_end = True
                    subscription.save()

                    # Update the user_subscription model. Subscription is still active until the end of the period is
                    # reached
                    user_subscription.date_cancelled = datetime.fromtimestamp(subscription.current_period_end)
                    user_subscription.status = SubscriptionOrder.StatusChoices.CANCELLED
                    user_subscription.save()
                    send_success_notification(request, title='Subscription cancelled',
                                              message='Your subscription has been successfully cancelled')

            except stripe.error.StripeError as e:
                send_error_notification(request, title='Error cancelling subscription',
                                        message='An error occurred while trying to cancel the subscription, please contact\
                                        support if the problem persists')

                logging.error('Error retrieving subscription')
                logging.error(e)

        else:
            # Todo - add better message and handling of this scenario
            send_error_notification(request, title='Error cancelling subscription',
                                    message='You do not have permission')

            # Handle error

        return redirect('subscriptions:subscription-plans')
