import logging

from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

# Retrieve the current user model
User = get_user_model()


# Views
class HomeView(TemplateView):
    """
    Returns the home page of the website.
    """
    template_name = 'core/home.html'


class TermsOfServiceView(TemplateView):
    """
    Handles the display of the terms of service page.
    """
    template_name = 'core/terms-of-service.html'


class TestView(TemplateView):
    """
    Test view for testing various items.
    """
    template_name = 'core/test.html'

    def get(self, request, *args, **kwargs):
        logging.debug('[MAIN.TEST] View is for testing various items.')
        context = {
            'data': 'This is my context data...',
        }
        return self.render_to_response(context)
