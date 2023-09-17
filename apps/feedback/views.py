import logging

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from apps.feedback.forms import FeedbackForm


# Create your views here.
@require_http_methods(['POST'])
def submit_feedback(request):
    """
    Handles feedback submission via POST method.

    This view function is designed to handle the submission of user feedback forms.
    Upon successful validation, it saves the form data to a new or existing Feedback
    model instance. A user must be authenticated to include additional user-specific data.

    Parameters:
        request (HttpRequest): The HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse: An HttpResponse object containing the rendered HTML of the
                      'components/forms/feedback/partials/success.html' template.

    Notes:
        - This function expects POST data containing 'content' and 'page_url' fields.
        - If the user is authenticated, additional user-specific data is saved.
    """
    logging.debug('[SUBMIT_FEEDBACK] called')

    feedback_form = FeedbackForm(request.POST)

    if feedback_form.is_valid():
        feedback_form.save(user=request.user if request.user.is_authenticated else None)
        return render(request, 'components/forms/feedback/partials/success.html')

    # HTML partial return
    return render(request, 'components/forms/feedback/partials/success.html')
