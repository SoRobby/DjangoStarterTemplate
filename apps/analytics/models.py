from uuid import uuid4

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from config import settings
from .signals import object_viewed_signal
from .utils import get_client_ip_address

User = settings.AUTH_USER_MODEL


# Create your models here.

class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                             help_text='User that the session is associated with')

    session_key = models.CharField(max_length=40, blank=True, null=True, help_text='Session key')

    is_session_active = models.BooleanField(default=True, help_text='Is the session active?')

    # session_duration = models.IntegerField(help_text='Session duration in seconds')

    # session_data onload
    # session data beforeunload

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the session')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created',
                                        help_text='Server date and time when the item was created modified')

    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified',
                                         help_text='Server date and time when the item was last modified')


class PageViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                             help_text='The user that viewed the page')

    user_session = models.ForeignKey(UserSession, blank=True, null=True, on_delete=models.SET_NULL,
                                     help_text='The user session that the page was viewed in')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the session')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created',
                                        help_text='Server date and time when the item was created modified')

    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified',
                                         help_text='Server date and time when the item was last modified')


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                             help_text='User that viewed the object')

    user_session = models.ForeignKey(UserSession, blank=True, null=True, on_delete=models.SET_NULL,
                                     help_text='User session that the object was viewed in')

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, help_text='Content type')

    object_id = models.PositiveIntegerField(help_text='Content type object id')

    content_object = GenericForeignKey('content_type', 'object_id')

    ip_address = models.CharField(max_length=120, blank=True, null=True, help_text='IP address of the user')

    timestamp = models.DateTimeField(auto_now_add=True, help_text='Date and time when the object was viewed')


    def __str__(self, ):
        return str(f'{self.content_object} ({self.timestamp})')

    @property
    def name_of_user(self):
        if self.user:
            return self.user.username
        return 'AnonymousUser'

    def get_content_object_url(self):
        return self.content_object.get_absolute_url()

    class Meta:
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'
        ordering = ['-timestamp']


# analytics/models.py


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    ip_address = get_client_ip_address(request) if hasattr(request, 'META') else None

    ObjectViewed.objects.create(
        user=request.user,
        content_type=c_type,
        object_id=instance.id,
        ip_address=ip_address
    )


object_viewed_signal.connect(object_viewed_receiver)
