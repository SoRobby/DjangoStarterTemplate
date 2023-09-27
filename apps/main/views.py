import logging
import traceback

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from apps.blog.models import Post

User = get_user_model()


# Create your views here.
def home(request: HttpResponse) -> HttpResponse:
    context = {}
    logging.debug('This is my home page...')

    # posts = Post.objects.published()
    posts = Post.objects.all()
    context['posts'] = posts

    return render(request, 'main/home.html', context)


def test(request: HttpResponse) -> HttpResponse:
    context = {}
    logging.debug('[MAIN.TEST] View is for testing various items.')
    return render(request, 'main/test.html', context)

def terms_of_service(request):
    return render(request, 'main/terms-of-service.html')


# HTTP status codes
def handle400(request, exception):
    """
    Handles HTTP 400 Bad Request errors by rendering a custom HTML
    template and returning the result to the requesting client.
    """
    return render(request, 'main/status_codes/400.html')


def handle403(request, exception):
    """
    Handles HTTP 403 Forbidden errors by rendering a custom HTML
    template and returning the result to the requesting client.
    """
    return render(request, 'main/status_codes/403.html')


def handle404(request, exception):
    """
    Handles HTTP 404 Not Found errors by rendering a custom HTML
    template and returning the result to the requesting client.
    """
    return render(request, 'main/status_codes/404.html')


def handle500(request, *args, **argv):
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

    return render(request, 'main/status_codes/500.html', context)
