"""
Accounts utility (utils.py) functions for the accounts app.
"""


def get_redirect_if_exists(request):
    """
    Extracts 'next' parameter from request GET data, used for redirecting after login.

    Args:
        request (HttpRequest): The current request.

    Returns:
        str: Redirect URL if 'next' exists, otherwise None.
    """
    redirect = None

    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))

    return redirect
