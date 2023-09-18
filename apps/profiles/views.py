import logging

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, UpdateView

from apps.accounts.models import Account
from apps.accounts.services import send_verification_email
from apps.main.models import Country
from libs.utils.utils import send_notification
from .forms import ProfileEditGeneralForm, ChangeEmailForm, SupportMessageForm
from .services import send_support_email


# Create your views here.
# def profile(request, *args, **kwargs):
#     return render(request, 'accounts/profile/profile.html')
class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'


# class ProfileEditGeneralView(TemplateView):
#     template_name = 'avatar/profile-edit-general.html'

class ProfileEditGeneralView(UpdateView):
    model = Account
    form_class = ProfileEditGeneralForm
    template_name = 'profiles/edit/profile-edit-general.html'

    def get_object(self, queryset=None):
        logging.debug('[PROFILE_EDIT_SECURITY_CHANGE_EMAIL] Called')
        return self.request.user

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        return context

    # Return success URL to itself
    def get_success_url(self):
        send_notification(self.request, tag='success', title='Settings updated',
                          message='Your settings have been successfully updated')
        return self.request.path


class ProfileEditSecurityView(TemplateView):
    template_name = 'profiles/edit/profile-edit-security.html'


@login_required
@require_http_methods(['POST'])
def profile_edit_security_change_email(request, *args, **kwargs):
    logging.debug('[PROFILE_EDIT_SECURITY_CHANGE_EMAIL] Called')

    form = ChangeEmailForm(request.POST)
    user = request.user
    username = request.POST.get('username', None)

    if username == user.username:
        if form.is_valid():
            form.save(request.user)
            domain = get_current_site(request).domain
            send_verification_email(user, domain)
            send_notification(request, tag='success', title='Email changed',
                              message='Email address changed, please verify the new email')
        else:
            logging.error(f'Form is invalid\n\tError: {form.errors}')
            send_notification(request, tag='error', title='Email already in use',
                              message='The changed email address is already in use')
    else:
        logging.error('Username does not match the logged-in user')
        send_notification(request, tag='error', title='Unauthorized',
                          message='You are not authorized to change the email for this account')

    return redirect('profiles:settings-security')


class ProfileEditNotificationsView(TemplateView):
    template_name = 'profiles/edit/profile-edit-notifications.html'


class ProfileEditSupportView(TemplateView):
    template_name = 'profiles/edit/profile-edit-support.html'


@login_required
@require_http_methods(['POST'])
def profile_edit_support_send_message(request, *args, **kwargs):
    logging.debug('[PROFILE_EDIT_SUPPORT_SEND_MESSAGE] Called')

    form = SupportMessageForm(request.POST)

    if form.is_valid():
        try:
            send_support_email(
                form.cleaned_data['name'],
                form.cleaned_data['email'],
                form.cleaned_data['subject'],
                form.cleaned_data['message']
            )
            send_notification(request, tag='success', title='Message sent',
                              message='Your message has been successfully sent')
        except Exception as e:
            logging.error(f'Error occurred while trying to send support email.\n\tError: {e}')
            if request.user.is_staff:
                send_notification(request, tag='error', title='Unable to send message',
                                  message=f'There was an error sending the message, please try again later.\nError: {e}')
            else:
                send_notification(request, tag='error', title='Unable to send message',
                                  message='There was an error sending the message, please try again later')

    else:
        logging.error(f'Form is invalid\n\tError: {form.errors}')
        if request.user.is_staff:
            send_notification(request, tag='error', title='Unable to send message',
                              message=f'There was an error sending the message, please try again later.\nError: {form.errors}')
        else:
            send_notification(request, tag='error', title='Unable to send message',
                              message='There was an error sending the message, please try again later')

    return redirect(request.META.get('HTTP_REFERER', 'default-page-if-no-referer'))
