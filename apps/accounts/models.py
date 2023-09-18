from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save

from apps.accounts.managers import AccountManager


# Models
class Account(AbstractBaseUser):
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

    description = models.TextField(max_length=500, blank=True, verbose_name='Description',
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
    profile_image = models.ImageField(upload_to='accounts/', blank=True, null=True, verbose_name='Profile image',
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

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label) -> bool:
        return True

    @property
    def theme_choices_as_list(self):
        return [{'key': key, 'name': name} for i, (key, name) in enumerate(self.ThemeChoices.choices)]

    def generate_new_email_verification_token(self):
        self.email_verification_token = uuid4()
        self.save()

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


# Signal group for generating short uuid
def generate_short_uuid(instance, length=8):
    """
    Recursive function that generates a unique short uuid of a given length.
    """
    short_uuid = str(uuid4()).replace('-', '')[:length].lower()
    instances = instance.__class__.objects.filter(short_uuid=short_uuid)

    if len(instances) > 0:
        short_uuid = generate_short_uuid(length)
    return short_uuid


def pre_save_account_receiver(sender, instance, *args, **kwargs):
    if not instance.short_uuid:
        instance.short_uuid = generate_short_uuid(instance, length=instance._meta.get_field('short_uuid').max_length)


pre_save.connect(pre_save_account_receiver, sender=Account)
