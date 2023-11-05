from django.shortcuts import render

from .models import SubscriptionPlan, SubscriptionTerm

# Create your views here.
def subscription_plans(request):
    context = {}

    context['subscription_plans'] = SubscriptionPlan.objects.filter(is_active=True)

    for plan in SubscriptionPlan.objects.filter(is_active=True):
        features = plan.features
        # print(type(features))
        # print(features)

    return render(request, 'subscriptions/plans.html', context)

