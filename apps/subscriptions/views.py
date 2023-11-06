import logging
import urllib
import urllib.parse

import stripe
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from apps.core.utils import send_error_notification
from .models import SubscriptionPlan, SubscriptionTerm, SubscriptionOrder

# Set the api key
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def subscription_plans(request):
    context = {}
    plan_category = SubscriptionPlan.PlanCategories.DEFAULT

    subscription_plans = SubscriptionPlan.objects.active().filter(plan_category=plan_category)
    subscription_terms = SubscriptionTerm.objects.active().filter(subscription_plan__in=subscription_plans).order_by(
        'price_cents')

    monthly_plans = SubscriptionTerm.objects.active_monthly(plan_category=plan_category)
    annual_plans = SubscriptionTerm.objects.active_annual(plan_category=plan_category)

    context['monthly_plans'] = monthly_plans
    context['annual_plans'] = annual_plans
    context['subscription_plans'] = subscription_plans

    logging.debug(f'monthly_plans = {monthly_plans}')
    logging.debug(f'annual_plans = {annual_plans}')
    logging.debug(f'subscription_plans = {subscription_plans}')

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
        term = get_object_or_404(SubscriptionTerm, uuid=term_uuid)
        logging.debug(f'Selected term = {term}')

        # User purchasing
        purchaser = request.user

        try:
            order = SubscriptionOrder.objects.create(
                purchaser=purchaser,
                subscription_term=term,
                purchase_status=SubscriptionOrder.PurchaseStatusChoices.PENDING,
            )

            # Set the stripe variables
            success_partial_url = reverse('home')
            success_url = urllib.parse.urljoin(domain_partial_url, success_partial_url)

            # If the user cancels the payment, the cancel url will retrieve the order by uuid and set the status to
            # cancelled
            print(f'term_uuid = {term_uuid}')
            print(f'order.uuid = {order.uuid}')

            cancel_partial_url = reverse('subscriptions:subscription-checkout-cancel', kwargs={
                'term_uuid': term_uuid,
                'order_uuid': order.uuid
            })

            print(f'cancel_partial_url = {cancel_partial_url}')
            cancel_url = urllib.parse.urljoin(domain_partial_url, cancel_partial_url)



            # Format the Stripe payment request

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': term.stripe_price_id,  # e.g. price_1KVqZYGH7IAkWYyXOExqnpAw
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url + '?session_id={CHECKOUT_SESSION_ID}',
                customer_email=purchaser.email,

            )

            # Set the api key

            return HttpResponseRedirect(checkout_session.url)

            logging.debug('SubscriptionOrder created')
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

# CheckoutSessionCreateView
