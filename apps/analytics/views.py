# Create your views here.
import logging

from django.http import JsonResponse


def analytics_onload_endpoint(request):
    logging.debug('[ANALYTICS.ANALYTICS_ONLOAD_ENDPOINT] Called')
    # return HttpResponse('Analytics endpoint')
    return JsonResponse({"message": "ANALYTICS.ANALYTICS_ONLOAD_ENDPOINT"})


def analytics_beforeunload_endpoint(request):
    logging.debug('[ANALYTICS.ANALYTICS_BEFOREUNLOAD_ENDPOINT] Called')
    # return HttpResponse('Analytics endpoint')
    return JsonResponse({"message": "ANALYTICS.ANALYTICS_BEFOREUNLOAD_ENDPOINT"})
