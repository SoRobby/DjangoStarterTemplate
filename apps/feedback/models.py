from uuid import uuid4

from django.conf import settings
from django.db import models

from db.abstract_models import DateCreatedAndModified


# Create your models here.
class Feedback(DateCreatedAndModified):
    class CATEGORY(models.TextChoices):
        BUG = 'bug', 'Bug Report'
        FEATURE = 'feature', 'Feature Request'
        GENERAL = 'general', 'General Feedback'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=255, blank=True, null=True,
                            help_text='Name of the individual providing feedback')

    email = models.EmailField(max_length=255, blank=True, null=True,
                              help_text='Email of the individual providing feedback')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='feedback_user',
                             on_delete=models.SET_NULL, help_text='User that provided feedback')

    page_url = models.URLField(max_length=255, blank=True, null=True,
                               help_text='URL of the page where feedback was provided')

    category = models.CharField(max_length=55, default=CATEGORY.GENERAL, choices=CATEGORY.choices,
                                help_text='Category of the feedback')

    content = models.TextField(max_length=3000, blank=True, null=True, help_text='Content of the feedback')

    is_processed = models.BooleanField(default=False, help_text='Whether the feedback has been processed or not')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the feedback')

    def __str__(self):
        return f'Feedback {self.pk}'

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'
        ordering = ('-date_created',)
