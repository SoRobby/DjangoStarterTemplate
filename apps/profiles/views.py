import logging
from PIL import Image
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, DetailView

from apps.accounts.forms import AccountSettingsForm
from apps.accounts.models import Account, AccountSettings
from apps.accounts.services import send_verification_email
from apps.core.utils import send_success_notification, send_error_notification
from apps.core.utils import str_to_bool
from apps.subscriptions.models import SubscriptionOrder
from apps.subscriptions.services import SubscriptionService
from .forms import ChangeEmailForm, SupportMessageForm
from .services import send_support_email
from apps.core.utils import process_image, save_file_to_field
from apps.accounts.utils import upload_to_profile_images


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

class ProfileEditGeneralView(LoginRequiredMixin, TemplateView):
    model = Account
    template_name = 'profiles/edit/general.html'

    def get(self, request, *args, **kwargs):
        logging.debug('[PROFILE_EDIT_GENERAL_VIEW.GET] Called')
        context = {}
        context['user'] = request.user
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        logging.debug('[PROFILE_EDIT_GENERAL_VIEW.POST] Called')

        # Get data
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        is_profile_public = str_to_bool(request.POST.get('is_profile_public', None))

        profile_image = request.FILES.get('profile_image')
        print(f'profile_image = {profile_image}')

        user = request.user
        user.name = name
        user.description = description
        user.is_profile_public = is_profile_public
        user.save()


        if 'cropper-distance-x' in request.POST:
            if request.POST.get('cropper-distance-x') != '':
                image_crop_x = float(request.POST.get('cropper-distance-x'))
                image_crop_y = float(request.POST.get('cropper-distance-y'))
                image_crop_width = float(request.POST.get('cropper-width'))
                image_crop_height = float(request.POST.get('cropper-height'))

                crop_dimensions = (image_crop_x, image_crop_y, image_crop_width, image_crop_height)

                logging.debug('[EDIT_POST] Cropper values are not empty')
                logging.debug(f'[EDIT_POST] image_crop_x = {image_crop_x}')
                logging.debug(f'[EDIT_POST] image_crop_y = {image_crop_y}')
                logging.debug(f'[EDIT_POST] image_crop_width = {image_crop_width}')
                logging.debug(f'[EDIT_POST] image_crop_height = {image_crop_height}')

                if image_crop_width / image_crop_height != user.PROFILE_IMAGE_ASPECT_RATIO:
                    logging.warning(f'[EDIT_ARTICLE] Incorrect image aspect ratio')
                else:
                    logging.debug(f'[EDIT_ARTICLE] Correct image aspect ratio')

                # Get image file that was uploaded
                profile_image_raw = Image.open(request.FILES.get('profile_image'))

                # Featured image logic
                profile_image_raw_file = process_image(
                    image=profile_image_raw,
                    crop_dimensions=None,
                    resize_dimensions=None,
                    file_format=None,
                )

            #     save_file_to_field(
            #         model_instance=article,
            #         field_name='featured_image_raw',
            #         file=featured_image_raw_file,
            #         directory_path=upload_to_featured_images(article, None),
            #         file_name=f'raw.{featured_image_raw.format.lower()}'
            #     )
            #     # blog_post.featured_image_raw.save(f'raw-{current_datetime}.{featured_image_raw.format.lower()}',\
            #     # featured_image_raw_file)
            #
                # Featured image logic
                process_image(
                    image=profile_image_raw,
                    crop_dimensions=crop_dimensions,
                    resize_dimensions=user.PROFILE_IMAGE_SIZE,
                    file_format='png'
                )
                save_file_to_field(
                    model_instance=user,
                    field_name='profile_image',
                    file=profile_image_raw_file,
                    directory_path=upload_to_profile_images(user, None),
                    file_name=f'featured.webp'
                )
            #     # blog_post.featured_image.save(f'featured-{current_datetime}.webp', featured_image_file)
            #
            #     # Featured image thumbnail logic
            #     featured_image_thumbnail_file = process_image(
            #         image=featured_image_raw,
            #         crop_dimensions=crop_dimensions,
            #         resize_dimensions=article.FEATURED_IMAGE_THUMBNAIL_SIZE,
            #         file_format='png'
            #     )
            #     save_file_to_field(
            #         model_instance=article,
            #         field_name='featured_image_thumbnail',
            #         file=featured_image_thumbnail_file,
            #         directory_path=upload_to_featured_images(article, None),
            #         file_name=f'thumbnail.webp'
            #     )
            #     # blog_post.featured_image_thumbnail.save(f'thumbnail-{current_datetime}.webp',\
            #     # featured_image_thumbnail_file)
            #
            #     article.save()
            #
            # else:
            #     logging.debug('[EDIT_POST] Cropper values are empty and no image was uploaded')

        send_success_notification(self.request, title='Settings updated',
                                  message='Your settings have been successfully updated')

        return redirect('profiles:settings-general')

    # def get_success_url(self):
    #     send_success_notification(self.request, title='Settings updated',
    #                               message='Your settings have been successfully updated')

    # return self.request.path


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
        user_subscription_order = SubscriptionOrder.objects.filter(purchaser=self.request.user, is_active=True)

        if user_subscription_order:
            user_subscription_order = user_subscription_order.first()
            SubscriptionService.verify_stripe_subscription(user_subscription_order)

        user_subscription_order = SubscriptionOrder.objects.filter(purchaser=self.request.user, is_active=True)
        print(f'user_subscription_order = {user_subscription_order}')

        if user_subscription_order:
            print("GETTING IT!!!!")
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
