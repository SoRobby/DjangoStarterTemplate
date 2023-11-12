from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from .managers import FeedbackManager


# Models
class Feedback(BaseModel):
    class CATEGORY(models.TextChoices):
        BUG = 'bug', 'Bug Report'
        FEATURE = 'feature', 'Feature Request'
        GENERAL = 'general', 'General Feedback'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Name',
                            help_text='Name of the individual providing feedback')

    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Email',
                              help_text='Email of the individual providing feedback')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='feedback_user',
                             on_delete=models.SET_NULL, verbose_name='User', help_text='User that provided feedback')

    page_url = models.URLField(max_length=255, blank=True, null=True, verbose_name='Page URL',
                               help_text='URL of the page where feedback was provided')

    category = models.CharField(max_length=55, default=CATEGORY.GENERAL, choices=CATEGORY.choices,
                                verbose_name='Category', help_text='Category of the feedback')

    content = models.TextField(max_length=3000, verbose_name='Content', help_text='Content of the feedback')

    is_processed = models.BooleanField(default=False, verbose_name='Is processed',
                                       help_text='Whether the feedback has been processed or not')

    objects = FeedbackManager()

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        return f'Feedback {self.pk}'
