from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from config import settings
from .signals import object_viewed_signal
from .utils import get_client_ip_address

User = settings.AUTH_USER_MODEL


# Create your models here.
class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                             help_text='User that viewed the object')

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, help_text='Content type')

    object_id = models.PositiveIntegerField(help_text='Content type object id')

    content_object = GenericForeignKey('content_type', 'object_id')

    ip_address = models.CharField(max_length=120, blank=True, null=True, help_text='IP address of the user')

    timestamp = models.DateTimeField(auto_now_add=True, help_text='Date and time when the object was viewed')

    def __str__(self, ):
        return str(f'{self.content_object} ({self.timestamp})')

    class Meta:
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'
        ordering = ['-timestamp']


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
