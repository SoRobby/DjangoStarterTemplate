import logging
import uuid

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.safestring import mark_safe

from apps.accounts.forms import AccountAuthenticationForm, RegistrationForm
from apps.accounts.services import send_verification_email
from apps.accounts.utils import get_redirect_if_exists
from apps.core.utils import send_error_notification, send_success_notification

# Set the user model
User = get_user_model()


# Function based views:
def login_view(request, *args, **kwargs):
    """
    Attempts to authenticate the user and logs them in if successful.
    """
    logging.debug('[LOGIN_VIEW] called')
    context = {}
    default_redirect = 'home'
    user = request.user

    # If the user is already authenticated/logged they are redirected to homepage
    if user.is_authenticated:
        return redirect(default_redirect)

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        email = request.POST['email']

        if form.is_valid():
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            a = 0/1

            if user:
                login(request, user)

                # See if a redirection exists in the session (e.g. if the user tried to access a page that required
                # authentication)
                # Example of a redirection url, '/accounts/login/?next=/accounts/profile/'
                # TODO - Need to verify that the redirect url is on the same domain for security reasons.
                destination = get_redirect_if_exists(request)

                if destination:
                    return redirect(destination)
                else:
                    return redirect(default_redirect)
        else:
            # Pass errors to frontend
            try:
                # Check if an account with that email exists
                User.objects.get(email=email)
                context['login_error'] = mark_safe(
                    'Wrong password, try again or click <span class="italic">Forgot password</span> to reset it')
            except:
                context['login_error'] = 'An account with that email does not exist'
            context['login_form'] = form

    return render(request, 'accounts/login.html', context)


def logout_view(request):
    """
    Logs the user out and redirects the user to the homepage.
    """
    logging.debug('[LOGOUT_VIEW] called')
    logout(request)
    return redirect('home')


def register_view(request, *args, **kwargs):
    """
    Creates a new account for the user if the form is valid.
    """
    logging.debug('[REGISTER_VIEW] Called')
    context = {}
    user = request.user

    # If the user is already authenticated/logged in they are redirected to homepage
    if user.is_authenticated:
        return redirect('home')
    else:
        if request.POST:
            form = RegistrationForm(request.POST)

            if form.is_valid():
                form.save()

                # Get the cleaned form data that will be used to authenticate the
                # user and log them in
                email = form.cleaned_data.get('email').lower()
                raw_password = form.cleaned_data.get('password1')

                # Next log the user in
                user = authenticate(email=email, password=raw_password)
                login(request, user)

                # Check to see if user is logged in:
                if user.is_authenticated:
                    # Get the current domain
                    domain = get_current_site(request).domain

                    # Send verification email to user
                    send_verification_email(user, domain)

                    destination = get_redirect_if_exists(request)
                    if destination:
                        return redirect(destination)
                    else:
                        return redirect('home')
                else:
                    logging.error(
                        '[REGISTER_VIEW] User is not authenticated even though form is valid and account was created')
                    return redirect('home')
            else:
                context['registration_form'] = form

        return render(request, 'accounts/register.html', context)


def send_verification_email_view(request, username: str):
    logging.debug('[SEND_VERIFICATION_EMAIL] Called')
    if request.user.username == username or request.user.is_superuser:

        user = User.objects.get(username=username)
        user.generate_new_email_verification_token()

        try:
            # Get the current domain
            domain = get_current_site(request).domain

            # Send verification email to user
            send_verification_email(user, domain)

            # Send notification to user
            send_success_notification(request, title='Verification email sent',
                                      message=f'Verification email has been sent to "{user.email}"')

        except Exception as e:
            # Send error notification to user. If user is staff, show error message in notification
            if request.user.is_staff:
                send_error_notification(request, title='Unable to send verification email',
                                        message=f'We were unable to send the verification email due to an unexpected\
                                        error\nError: {e}')

            else:
                send_error_notification(request, title='Unable to send verification email',
                                        message='We were unable to send the verification email due to an unexpected\
                                        error')

        # Redirect to the same page
        return redirect(request.META.get('HTTP_REFERER', 'default-page-if-no-referer'))
    else:
        return redirect('home')


def verify_email(request, token):
    logging.debug('[VERIFY_EMAIL] Called')

    try:
        # Decode the token
        decoded_token = force_str(urlsafe_base64_decode(token))
        user = User.objects.get(email_verification_token=uuid.UUID(decoded_token))

        # Verify user's email
        if not user.email_verified:
            user.email_verified = True
            user.save()
            send_notification(request, tag='success', title='Email verified',
                              message=f'Your email has been successfully verified')

            return redirect('home')
        else:
            send_notification(request, tag='success', title='Email already verified',
                              message=f'Your email has already been verified')
            return redirect('home')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        if request.user.is_staff:
            send_notification(request, tag='error', title='Invalid verification token',
                              message=f'The token is has expired and is no longer valid, resend the verification email\nError: {e}')
        else:
            send_notification(request, tag='error', title='Invalid verification token',
                              message='The token is has expired and is no longer valid, resend the verification email')

        return redirect('home')


def soft_delete_account_view(request):
    if request.user.is_authenticated and request.method == 'POST':

        # Try to delete the user
        try:
            current_user = User.objects.get(username=request.user.username)
            current_user.is_marked_for_deletion = True
            current_user.save()
            logout(request)
            send_notification(request, tag='success', title='Account deleted',
                              message='Your account is set to be deleted 14 days from now')

        except User.DoesNotExist:
            send_notification(request, tag='error', title='Error when deleting account',
                              message='There was an error when attempting to delete your account')
            return JsonResponse({"error": "User does not exist."}, status=400)

    return redirect('home')


def hard_delete_account_view(request):
    if request.user.is_authenticated and request.method == 'POST':

        # Try to delete the user
        try:
            current_user = User.objects.get(username=request.user.username)
            current_user.delete()
            send_notification(request, tag='success', title='Account deleted',
                              message='Your account has been deleted')

        except User.DoesNotExist:
            send_notification(request, tag='error', title='Error when deleting account',
                              message='There was an error when attempting to delete your account')
            return JsonResponse({"error": "User does not exist."}, status=400)

    return redirect('home')
