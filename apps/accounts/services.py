from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_verification_email(user: get_user_model(), domain: str):
    """
    Send a verification email to the user.

    Parameters:
    user (get_user_model()): User object from Account model.
    domain (str): The domain in which the user exists.

    Returns:
    None
    """

    # Check to see if email_verification_token exists, if it doesn't create it
    # By default, email_verification_token should exist.
    if not user.email_verification_token:
        user.email_verification_token = uuid4()
        user.save()

    # Create an url safe encoded token based on the email_verification_token uuid
    token = urlsafe_base64_encode(force_bytes(user.email_verification_token))

    # Format email
    mail_subject = 'Verify your email'
    message = render_to_string('accounts/registration/verify_email.html', {
        'user': user,
        'domain': domain,
        'token': token,
    })

    # Send email to user's email
    send_mail(mail_subject, message, settings.EMAIL_ADDRESSES['NO_REPLY'], [user.email])
