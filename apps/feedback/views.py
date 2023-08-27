import logging
import traceback

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from apps.feedback.models import Feedback

User = get_user_model()


# Create your views here.
@require_http_methods(['POST'])
def submit_feedback(request):
    print('Feedback submitted')

    # Get the feedback POST data
    feedback_content = request.POST.get('feedback', None)
    current_url = request.POST.get('current_url', None)

    # Save feedback data to the model Feedback
    Feedback.objects.create(content=feedback_content, page_url=current_url)

    # Print all POST data
    for key, value in request.POST.items():
        logging.debug(f'{key}: {value}')

    # HTML partial return
    return render(request, 'components/forms/feedback/partials/success.html')

    # Return a blank response that is success
    # return HttpResponse()


