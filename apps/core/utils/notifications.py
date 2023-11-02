from django.contrib import messages


def send_notification(request, tag: str, title: str = '', message: str = '') -> None:
    """
    Adds a formatted message to the Django messages framework based on the provided tag.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        tag (str): The tag that determines the message level. Valid options are 'info', 'success', 'warning', 'error'.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    message_levels = {
        'info': messages.INFO,
        'success': messages.SUCCESS,
        'warning': messages.WARNING,
        'error': messages.ERROR,
    }
    level = message_levels.get(tag, None)
    messages.add_message(request, level=level, message=message, extra_tags=title)


def send_info_notification(request, title: str = '', message: str = '') -> None:
    """
    Adds an info message to the Django messages framework.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    send_notification(request, tag='info', title=title, message=message)


def send_success_notification(request, title: str = '', message: str = '') -> None:
    """
    Adds a success message to the Django messages framework.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    send_notification(request, tag='success', title=title, message=message)


def send_warning_notification(request, title: str = '', message: str = '') -> None:
    """
    Adds a warning message to the Django messages framework.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    send_notification(request, tag='warning', title=title, message=message)


def send_error_notification(request, title: str = '', message: str = '') -> None:
    """
    Adds an error message to the Django messages framework.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    send_notification(request, tag='error', title=title, message=message)
