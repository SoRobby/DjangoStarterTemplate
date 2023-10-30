from uuid import uuid4

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.contrib.sessions.models import Session

from config import settings
from .signals import object_viewed_signal
from .utils import get_client_ip_address


# Models

class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             help_text='User that the session is associated with')

    session_key = models.CharField(max_length=40, help_text='Session key')

    is_session_active = models.BooleanField(default=True, help_text='Is the session active?')

    session_data_onload = models.JSONField(blank=True, null=True, help_text='Session data onload')

    session_data_beforeunload = models.JSONField(blank=True, null=True, help_text='Session data beforeunload')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the session')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created',
                                        help_text='Server date and time when the item was created modified')

    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified',
                                         help_text='Server date and time when the item was last modified')

    date_session_ended = models.DateTimeField(auto_now=True, verbose_name='Date session ended',
                                              help_text='Server date and time when the session ended')

    expire_date = models.DateTimeField(blank=True, null=True, help_text='Date and time when the session expires')

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'User session'
        verbose_name_plural = 'User sessions'

    def __str__(self) -> str:
        return str(f'{self.pk} ({self.session_key})')

    def save(self, *args, **kwargs):
        # Set the date_session_ended field
        if not self.is_session_active and self.date_session_ended is None:
            self.date_session_ended = timezone.now()
        elif self.is_session_active and self.date_session_ended is not None:
            self.date_session_ended = None

        # Call the original save method of models.model
        super().save(*args, **kwargs)

    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.is_session_active = False
            self.save()
        except Session.DoesNotExist:
            pass

        return self


class PageViewed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             help_text='User that viewed the object')

    user_session = models.ForeignKey(UserSession, blank=True, null=True, related_name='object_viewed',
                                     on_delete=models.SET_NULL, verbose_name='User session',
                                     help_text='User session that the object was viewed in')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True,
                                     verbose_name='Content type', help_text='Content type')

    object_id = models.PositiveIntegerField(help_text='Content type object id')

    content_object = GenericForeignKey('content_type', 'object_id')

    ip_address = models.CharField(max_length=120, blank=True, null=True, help_text='IP address of the user')

    date_viewed = models.DateTimeField(auto_now_add=True, help_text='Date and time when the object was viewed')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the object_viewed')

    class Meta:
        ordering = ['-date_viewed']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

    def __str__(self) -> str:
        return str(f'{self.content_object} ({self.date_viewed})')

    @property
    def name_of_user(self):
        if self.user:
            return self.user.username
        return 'AnonymousUser'

    def get_content_object_url(self):
        return self.content_object.get_absolute_url()


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
