from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_support_email(name: str, email: str, subject: str, message: str) -> None:
    """
    Sends a support email.

    Parameters:
    name (str): The sender's name.
    email (str): The sender's email.
    subject (str): The subject of the email.
    message (str): The content of the email.
    """

    # Format email
    mail_subject = f'Support Message - {subject}'
    mail_message = render_to_string('profiles/edit/emails/support-email.html', {
        'name': name,
        'message': message
    })

    # Send email to user's email
    send_mail(mail_subject, mail_message, 'noreply@your-domain.com', [email])

