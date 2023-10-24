import json
import logging

from django.contrib.contenttypes.models import ContentType
from django.urls import resolve
from django.utils import timezone

from .models import UserSession, ObjectViewed
from .registered_views import views_registry
from .utils import get_client_ip_address


def session_handler(request, user):
    """
    Handles user session creation and updates.

    Args:
        request (HttpRequest): The request object.
        user (User): The user object, or None if the user is unauthenticated.

    Returns:
        UserSession: The updated or newly created UserSession object.
    """
    # See if a session currently exists
    session_key_obj = request.session.session_key or request.session.create()

    # Get the current date and time
    now = timezone.now()

    # Get or create the UserSession object
    user_session, created = UserSession.objects.get_or_create(
        session_key=session_key_obj,
        user=user,
        expire_date__gte=now,
        defaults={
            'is_session_active': True,
            'expire_date': request.session.get_expiry_date()
        }
    )

    print(f'User session: {user_session}')

    if user_session:
        logging.debug(f'[SESSION_HANDLER] Updating existing session, session_key={user_session.session_key}')
        # if user_session.is_session_active is False:
        if user_session.is_session_active is False:
            user_session.is_session_active = True
            user_session.save(update_fields=['is_session_active', 'date_modified'])
    else:
        logging.debug('[SESSION_HANDLER] Creating new session')
        user_session = UserSession.objects.create(
            session_key=request.session.session_key,
            user=user,
            is_session_active=True,
            expire_date=request.session.get_expiry_date()
        )

    return user_session


class ObjectViewedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_viewed_object(request)
        return response

    def process_viewed_object(self, request):
        content_type = None

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

            if request.user.is_authenticated:
                user_session = session_handler(request=request, user=request.user)
            else:
                user_session = session_handler(request=request, user=None)

            # Assuming the identifier is a 'slug', adjust if using 'pk' or another identifier
            object_identifier = match.kwargs.get('slug')
            model_instance = content_type.model_class().objects.get(slug=object_identifier)

            ObjectViewed.objects.create(
                user=request.user if request.user.is_authenticated else None,
                content_type=content_type,
                object_id=model_instance.id,
                user_session=user_session,
                ip_address=get_client_ip_address(request),
            )

        except ContentType.DoesNotExist:
            logging.debug(
                f'ContentType does not exist for app_label={target_view["app_name"]},\
                model={target_view["model_name"]}')

        except Exception as e:
            if content_type and isinstance(e, content_type.model_class().DoesNotExist):
                logging.debug(f'Model instance does not exist for content_type={content_type}')
            else:
                logging.debug(f'Unexpected error: {str(e)}')


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
