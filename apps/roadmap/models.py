from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel
from .managers import FeatureManager


# Models
class Category(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Name', help_text='Name of the category')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug',
                            help_text='The URL slug based on the category name, slug fields should be 50 characters or\
                            less')

    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Description',
                                   help_text='Description of the category')

    class Meta:
        ordering = ['-name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'


class Feature(BaseModel):
    class ReleaseStatus(models.TextChoices):
        PLANNED = 'planned', 'Planned'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RELEASED = 'released', 'Released'
        ARCHIVED = 'archived', 'Archived'

    name = models.CharField(max_length=255, verbose_name='Name', help_text='Name of the feature')

    description = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Description',
                                   help_text='Description of the feature')

    category = models.ForeignKey(Category, null=True, blank=True, related_name='objective', on_delete=models.SET_NULL,
                                 verbose_name='Category', help_text='Category of the feature')

    release_status = models.CharField(max_length=255, choices=ReleaseStatus.choices, default=ReleaseStatus.PLANNED,
                                      verbose_name='Release status', help_text='Release status of the feature')

    up_votes = models.PositiveIntegerField(default=0, verbose_name='Up votes',
                                           help_text='Number of up votes for the feature')

    date_released = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                         verbose_name='Date released',
                                         help_text='Server date and time when the feature was released')

    date_archived = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                         verbose_name='Date archived',
                                         help_text='Server date and time when the feature was archived')

    objects = FeatureManager()

    class Meta:
        ordering = ['-name', '-date_created']
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'

    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'

    def save(self, *args, **kwargs):
        # Handle the date released
        if self.date_released is None and self.release_status == self.ReleaseStatus.RELEASED:
            self.date_released = timezone.now()
        elif self.date_released is not None and self.release_status != self.ReleaseStatus.RELEASED:
            self.date_released = None

        # Handle the date archived
        if self.date_archived is None and self.release_status == self.ReleaseStatus.ARCHIVED:
            self.date_archived = timezone.now()
        elif self.date_archived is not None and self.release_status != self.ReleaseStatus.ARCHIVED:
            self.date_archived = None

        # Call the original save method of models.model
        super().save(*args, **kwargs)
