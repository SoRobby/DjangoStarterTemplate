from django.conf import settings


def google_analytics_id(request):
    """
    Adds google analytics id to all requests
    """
    if settings.GOOGLE_ANALYTICS_ID:
        return {
            'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        }
    else:
        return {}
