import json
import logging

from django.contrib.contenttypes.models import ContentType
from django.urls import resolve

from .models import ObjectViewed
from .registered_views import views_registry


class ObjectViewedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_viewed_object(request)
        return response

    def process_viewed_object(self, request):
        # Determine the current URL's name and namespace
        match = resolve(request.path_info)
        current_url_name = match.url_name
        current_namespace = match.namespace

        # Find if this URL name and namespace exist in our registered views
        target_view = next(
            (view for view in views_registry.registered_views if
             view['url_name'] == current_url_name and view['namespace'] == current_namespace),
            None
        )

        # If the current URL isn't in the registered views, exit
        if not target_view:
            return

        # Fetch the content type and model instance based on the registered view details
        try:
            content_type = ContentType.objects.get(app_label=target_view['app_name'], model=target_view['model_name'])

            # Assuming the identifier is a 'slug', adjust if using 'pk' or another identifier
            object_identifier = match.kwargs.get('slug')
            model_instance = content_type.model_class().objects.get(slug=object_identifier)

            ObjectViewed.objects.create(
                user=request.user if request.user.is_authenticated else None,
                content_type=content_type,
                object_id=model_instance.id,
                # ... other fields ...
            )
        except (ContentType.DoesNotExist, content_type.model_class().DoesNotExist):
            pass

    # def process_viewed_object(self, request):
    #     # Determine the current URL's name and namespace
    #     match = resolve(request.path_info)
    #     url_name = match.url_name
    #     namespace = match.namespace
    #
    #     # Check if this URL name exists in our registered views
    #     target_view = next((view for view in VIEWS_TO_TRACK if
    #                         view['url_name'] == url_name and view['namespace'] == namespace), None)
    #     if not target_view:
    #         return
    #
    #     # Fetch the content type and model instance
    #     try:
    #         content_type = ContentType.objects.get(app_label=target_view['app_name'], model=target_view['model_name'])
    #
    #         object_identifier = match.kwargs.get('slug')  # Or 'pk' or other fields
    #         model_instance = content_type.model_class().objects.get(slug=object_identifier)
    #
    #         ObjectViewed.objects.create(
    #             user=request.user if request.user.is_authenticated else None,
    #             content_type=content_type,
    #             object_id=model_instance.id,
    #             # ... other fields
    #         )
    #     except (ContentType.DoesNotExist, content_type.model_class().DoesNotExist):
    #         pass


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before processing the view
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        # Print the current page
        logging.debug(f'Current page: {request.path}')

        logging.debug(f'\t\tSession key: {session_key}')

        # user_session, created = UserSession.objects.get_or_create(session_id=session_key)
        # if created:
        # # ... capture user, language, location, etc.
        #
        # Identify bots (simplest way, can be enhanced)

        # Get request meta information
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = request.META.get('REMOTE_ADDR', '')
        referer_url = request.META.get('HTTP_REFERER', '')
        host = request.META.get('HTTP_HOST', '')
        lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        user_cookie = request.COOKIES.get('cookie_name', '')

        # logging.debug(f'\t\tUser agent: {user_agent}')
        # logging.debug(f'\t\tIP address: {ip_address}')
        # logging.debug(f'\t\tReferer URL: {referer_url}')
        # logging.debug(f'\t\tHost: {host}')
        # logging.debug(f'\t\tLanguage: {lang}')
        # logging.debug(f'\t\tUser cookie: {user_cookie}')

        custom_header = request.META.get('HTTP_X_CUSTOM_HEADER', None)
        logging.debug(f'\t\tCustom header: {custom_header}')

        if request.method == 'POST' and custom_header:
            logging.debug('\t\tMETHOD: POST')
            data = json.loads(request.body.decode('utf-8'))
            logging.debug(f'\t\tUser analytic data: {data}')

        else:
            logging.debug('METHOD: GET')

        # data = json.loads(request.body.decode('utf-8'))
        # logging.debug(f'Body: {data}')
        #
        # current_time = data.get('currentTime', None)
        # user_agent = data.get('userAgent', None)
        #
        # logging.debug(f'Current time: {current_time}')
        # logging.debug(f'User agent: {user_agent}')

        # bots = ['bot', 'crawl', 'spider', 'slurp']
        # user_session.is_bot = any(bot in user_agent for bot in bots)
        # user_session.save()

        response = self.get_response(request)

        # After processing the view, e.g. updating end_time for a session

        return response
