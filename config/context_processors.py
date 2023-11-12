from django.conf import settings


def google_analytics_id(*args, **kwargs):
    """
    Adds google analytics id to all requests
    """
    if settings.GOOGLE_ANALYTICS_ID:
        return {'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID}
    else:
        return {}


def site_name(*args, **kwargs):
    """
    Adds the website name to all requests
    """
    if settings.SITE_NAME:
        return {'SITE_NAME': settings.SITE_NAME}
    else:
        return {}
