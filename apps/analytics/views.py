# Create your views here.
import logging
import json

from django.http import JsonResponse


def analytics_onload_endpoint(request):
    logging.debug('[ANALYTICS.ANALYTICS_ONLOAD_ENDPOINT] Called')

    custom_header = request.META.get('HTTP_X_CUSTOM_HEADER', None)
    logging.debug(f'\t\tCustom header: {custom_header}')

    if request.method == 'POST' and custom_header:
        # logging.debug('\t\tMETHOD: POST')
        data = json.loads(request.body.decode('utf-8'))
        # logging.debug(f'\t\tUser analytic data: {data}')
        # session_key = request.session.session_key
        # print(session_key)



    else:
        logging.debug('METHOD: GET')

    # return HttpResponse('Analytics endpoint')
    return JsonResponse({"message": "ANALYTICS.ANALYTICS_ONLOAD_ENDPOINT"})


def analytics_beforeunload_endpoint(request):
    logging.debug('[ANALYTICS.ANALYTICS_BEFOREUNLOAD_ENDPOINT] Called')
    # return HttpResponse('Analytics endpoint')
    return JsonResponse({"message": "ANALYTICS.ANALYTICS_BEFOREUNLOAD_ENDPOINT"})


