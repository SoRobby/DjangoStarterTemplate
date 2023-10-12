import json
import logging


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
        # logging.debug(f'\t\tCustom header: {custom_header}')

        if request.method == 'POST':
            logging.debug('\t\tMETHOD: POST')
            # logging.debug(f'test: {json.loads(request.body)}')
            body = json.loads(request.body.decode('utf-8'))
            logging.debug(f'\t\tData: {body}')

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
