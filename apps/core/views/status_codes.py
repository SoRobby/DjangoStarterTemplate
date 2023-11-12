import logging
import traceback

from django.shortcuts import render


# HTTP status codes
def handle400(request, *args, **kwargs):
    """
    Handles HTTP 400 Bad Request errors by rendering a custom HTML
    template and returning the result to the requesting client.
    """
    return render(request, 'core/status_codes/400.html')


def handle403(request, *args, **kwargs):
    """
    Handles HTTP 403 Forbidden errors by rendering a custom HTML
    template and returning the result to the requesting client.
    """
    return render(request, 'core/status_codes/403.html')


def handle404(request, *args, **kwargs):
    """
    Handles HTTP 404 Not Found errors by rendering a custom HTML
    template and returning the result to the requesting client.
    """
    return render(request, 'core/status_codes/404.html')


def handle500(request, *args, **kwargs):
    """
    Handles HTTP 500 Internal Server Error by rendering a custom HTML
    template and returning the result to the requesting client.
    """

    exception = traceback.format_exc()
    logger = logging.getLogger('django')
    logger.error('Server Error: %s', request.path,
                 extra={
                     'status_code': 500,
                     'request': request,
                     'exception': exception,
                 })

    if request.user.is_superuser:
        context = {'exception': exception}
    else:
        context = {}

    return render(request, 'core/status_codes/500.html', context)
