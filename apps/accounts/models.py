from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.accounts.managers import AccountManager
from apps.accounts.utils import generate_short_uuid, upload_to_profile_images



# Models
class Account(AbstractBaseUser):
    PROFILE_IMAGE_ASPECT_RATIO = 1 / 1
    PROFILE_IMAGE_SIZE = (300, 300)
    PROFILE_IMAGE_THUMBNAIL_SIZE = (100, 100)

    # Choice classes
    class ThemeChoices(models.TextChoices):
        LIGHT = 'light', 'Light'
        DARK = 'dark', 'Dark'
        SYSTEM = 'system', 'System'

    email = models.EmailField(max_length=255, unique=True, verbose_name='Email', help_text='Unique email address')

    username = models.CharField(max_length=16, unique=True,
                                validators=[
                                    RegexValidator(regex='^[a-zA-Z0-9_]*$',
                                                   message='Username must be alphanumeric or contain any of the'
                                                           ' following: "_"',
                                                   code='invalid_username'),
                                    MinLengthValidator(limit_value=4,
                                                       message='Username must be at least 4 characters long')
                                ],
                                verbose_name='Username', help_text='Unique username associated with the account')

    name = models.CharField(max_length=120, blank=True, verbose_name='Name', help_text='Name of the user')

    description = models.TextField(max_length=300, blank=True, verbose_name='Description',
                                   help_text='User bio or description')

    is_active = models.BooleanField(default=True, verbose_name='Active',
                                    help_text='Designates whether this user should be treated as active')

    is_staff = models.BooleanField(default=False, verbose_name='Staff status',
                                   help_text='Designates whether the user can log into this admin site')

    is_admin = models.BooleanField(default=False, verbose_name='Admin status',
                                   help_text='Designates whether the user can log into this admin site')

    is_superuser = models.BooleanField(default=False, verbose_name='Superuser status',
                                       help_text='Designates that this user has all permissions without explicitly '
                                                 'assigning them')

    # TODO - Make profile images upload the the uuid of the user.
    profile_image = models.ImageField(upload_to=upload_to_profile_images, blank=True, null=True, verbose_name='Profile image',
                                      help_text='Profile image or avatar')

    theme = models.CharField(max_length=55, default=ThemeChoices.SYSTEM, choices=ThemeChoices.choices,
                             verbose_name='Theme', help_text='User website theme')

    is_profile_public = models.BooleanField(default=True, verbose_name='Profile public',
                                            help_text='Designates whether the user profile can be viewed by others')

    email_verified = models.BooleanField(default=False, verbose_name='Email verified',
                                         help_text='Designates whether the user has verified their email address')

    email_verification_token = models.UUIDField(default=uuid4, editable=True, unique=True,
                                                verbose_name='Email verification token',
                                                help_text='Unique identifier for the email verification token')

    is_marked_for_deletion = models.BooleanField(default=False, verbose_name='Is marked for deletion',
                                                 help_text='Designates whether the user has marked their account for\
                                                 deletion')

    date_marked_for_deletion = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                                    verbose_name='Date marked for deletion',
                                                    help_text='Server date and time when the user deleted their\
                                                    account')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the account')

    short_uuid = models.CharField(max_length=8, unique=True, editable=False,
                                  validators=[
                                      MinLengthValidator(limit_value=8,
                                                         message='Short UUID must be exactly 8 characters long')
                                  ],
                                  verbose_name='Short UUID', help_text='Short unique identifier for the account'
                                  )

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date joined',
                                       help_text='Server date and time the account was created')

    last_login = models.DateTimeField(auto_now=True, verbose_name='Last login',
                                      help_text='Server date and time the account last logged in')

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name_plural = 'Accounts'
        verbose_name = 'Account'

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        # Set the date_deleted if the post is deleted
        if self.is_marked_for_deletion and self.date_marked_for_deletion is None:
            self.date_marked_for_deletion = timezone.now()

        # Call the original save method of models.model
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label) -> bool:
        return True

    def generate_new_email_verification_token(self):
        self.email_verification_token = uuid4()
        self.save()

    @property
    def theme_choices_as_list(self):
        return [{'key': key, 'name': name} for i, (key, name) in enumerate(self.ThemeChoices.choices)]

    @property
    def display_name(self):
        if self.is_profile_public and self.name:
            return self.name
        else:
            return self.username


    @staticmethod
    def get_theme_choices_as_dict():
        return dict(Account.ThemeChoices.choices)

    @staticmethod
    def get_theme_choices_as_list():
        """
        Returns the theme choices as a list of dictionaries with keys 'key' and 'name' for each choice.
        :return: list of dictionaries
        """
        return [{'key': key, 'name': name} for key, name in Account.ThemeChoices.choices]


class AccountSettings(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name='Account', related_name='settings',
                                   help_text='Account that is connected to the settings')

    show_email = models.BooleanField(default=False, verbose_name='Show email', help_text='Show or hide the email')

    receive_marketing_emails = models.BooleanField(default=True, verbose_name='Marketing emails',
                                                   help_text='Receive marketing emails')

    receive_weekly_digest_emails = models.BooleanField(default=True, verbose_name='Weekly digest emails',
                                                       help_text='Receive weekly digest emails')

    receive_discovery_emails = models.BooleanField(default=True, verbose_name='Discovery emails',
                                                   help_text='Receive emails about new features and tips')

    receive_site_update_emails = models.BooleanField(default=True, verbose_name='Site updates',
                                                     help_text='Receive site update emails')

    receive_inbox_message_notifications = models.BooleanField(default=True, verbose_name='Inbox message notifications',
                                                              help_text='Receive notifications when you receive a new\
                                                              message in your inbox')

    receive_announcement_notifications = models.BooleanField(default=True, verbose_name='Announcement notifications',
                                                             help_text='Receive notifications about new announcements')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the account settings')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created',
                                        help_text='Server date and time when the item was created modified')

    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified',
                                         help_text='Server date and time when the item was last modified')

    class Meta:
        verbose_name_plural = 'Account settings'
        verbose_name = 'Account setting'

    def __str__(self) -> str:
        return f"{self.account.username} settings"


# class AccountInteraction(models.Model):
#     account = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name='Account',
#                                    related_name='interactions', help_text='Account that is connected to the settings')


# Model signals
@receiver(pre_save, sender=Account)
def pre_save_account_receiver(sender, instance, *args, **kwargs):
    if not instance.short_uuid:
        instance.short_uuid = generate_short_uuid(instance, length=instance._meta.get_field('short_uuid').max_length)


@receiver(post_save, sender=Account)
def setup_account_tables(sender, instance, created, **kwargs):
    if created:
        AccountSettings.objects.create(account=instance)
