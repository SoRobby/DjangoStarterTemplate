import logging

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, UpdateView, DetailView

from apps.accounts.forms import AccountSettingsForm
from apps.accounts.models import Account, AccountSettings
from apps.accounts.services import send_verification_email
from apps.core.utils import send_success_notification, send_error_notification
from apps.subscriptions.models import SubscriptionOrder
from .forms import ProfileEditGeneralForm, ChangeEmailForm, SupportMessageForm
from .services import send_support_email


# Create your views here.
# def profile(request, *args, **kwargs):
#     return render(request, 'accounts/profile/profile.html')
class ProfileView(DetailView):
    model = Account
    template_name = 'profiles/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'


# class ProfileEditGeneralView(TemplateView):
#     template_name = 'avatar/general.html'

class ProfileEditGeneralView(UpdateView):
    model = Account
    form_class = ProfileEditGeneralForm
    template_name = 'profiles/edit/general.html'

    def get_object(self, queryset=None):
        logging.debug('[PROFILE_EDIT_GENERAL_VIEW.GET_OBJECT] Called')
        return self.request.user

    def get_context_data(self, **kwargs):
        logging.debug('[PROFILE_EDIT_GENERAL_VIEW.GET_CONTEXT_DATA] Called')
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        return context

    # Return success URL to itself
    def get_success_url(self):
        send_success_notification(self.request, title='Settings updated',
                                  message='Your settings have been successfully updated')

        return self.request.path


class ProfileEditSecurityView(TemplateView):
    template_name = 'profiles/edit/security.html'


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
            send_success_notification(request, title='Email changed',
                                      message='Email address changed, please verify the new email')

        else:
            logging.error(f'Form is invalid\n\tError: {form.errors}')
            send_error_notification(request, title='Email already in use',
                                    message='The changed email address is already in use')
    else:
        logging.error('Username does not match the logged-in user')
        send_error_notification(request, title='Unauthorized',
                                message='You are not authorized to change the email for this account')

    return redirect('profiles:settings-security')


class ProfileEditNotificationsView(TemplateView):
    model = AccountSettings
    template_name = 'profiles/edit/notifications.html'

    # Reference this https://chat.openai.com/c/3bcfc02f-81b2-4518-a0c8-b6bce02f5427
    # To finish this mode, got too tired to continue working on this. Falling asleep... zzzzz...

    def get_object(self, queryset=None):
        logging.debug('[PROFILE_EDIT_NOTIFICATIONS_VIEW.GET_OBJECT] Called')
        settings = AccountSettings.objects.get(account=self.request.user)
        return settings

    def get_context_data(self, **kwargs):
        logging.debug('[PROFILE_EDIT_NOTIFICATIONS_VIEW.GET_CONTEXT_DATA] Called')

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Get the settings object and add it to the context
        settings = self.get_object()
        context['settings'] = settings

        return context

    def post(self, request, *args, **kwargs):
        logging.debug('[PROFILE_EDIT_NOTIFICATIONS_VIEW.POST] Called')

        settings = self.get_object()
        settings_form = AccountSettingsForm(request.POST, instance=settings)

        if settings_form.is_valid():
            settings_form.save()
            send_success_notification(request, title='Settings updated',
                                      message='Your settings have been successfully updated')
        else:
            send_error_notification(request, title='Unable to save settings',
                                    message='There was an error saving your settings, please try again later')

        # Return the current page
        return self.get(request, *args, **kwargs)


class ProfileEditMembershipView(TemplateView):
    template_name = 'profiles/edit/membership.html'

    def get_context_data(self, **kwargs):
        logging.debug('[PROFILE_EDIT_MEMBERSHIP_VIEW.GET_CONTEXT_DATA] Called')
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Get subscription information if a user subscription exists
        user_subscription_order = SubscriptionOrder.objects.filter(purchaser=self.request.user)

        if user_subscription_order:
            user_subscription_order = user_subscription_order.first()
            logging.debug(user_subscription_order)
            context['user_subscription_order'] = user_subscription_order
            context['user_subscription_period'] = user_subscription_order.subscription_period
            context['user_subscription_plan'] = user_subscription_order.subscription_period.subscription_plan

        return context


class ProfileEditSupportView(TemplateView):
    template_name = 'profiles/edit/support.html'


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
            send_success_notification(request, title='Message sent', message='Your message has been successfully sent')

        except Exception as e:
            logging.error(f'Error occurred while trying to send support email.\n\tError: {e}')
            if request.user.is_staff:
                send_error_notification(request, title='Unable to send message',
                                        message=f'There was an error sending the message, please try again later.\
                                        \nError: {e}')
            else:
                send_error_notification(request, title='Unable to send message',
                                        message='There was an error sending the message, please try again later')

    else:
        logging.error(f'Form is invalid\n\tError: {form.errors}')
        if request.user.is_staff:
            send_error_notification(request, title='Unable to send message', message=f'There was an error sending the\
            message, please try again later.\nError: {form.errors}')
        else:
            send_error_notification(request, title='Unable to send message',
                                    message='There was an error sending the message, please try again later')

    return redirect(request.META.get('HTTP_REFERER', 'default-page-if-no-referer'))
