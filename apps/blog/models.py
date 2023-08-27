from math import ceil
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

from libs.utils.utils import generate_unique_slug
from .managers import PostManager


# Create your models here.

class Post(models.Model):
    class STATUS(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        REVIEW = 'review', 'Review'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=200, help_text='The title of the post')

    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True,
                            help_text='The URL slug based on the post title, slug fields should be 50 characters or\
                            less')

    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts', help_text='Post authors.')

    status = models.CharField(max_length=55, default=STATUS.DRAFT, choices=STATUS.choices, verbose_name='Status',
                              help_text='Current status of the post')

    content = CKEditor5Field(config_name='extends', verbose_name='Content',
                             help_text='Primary content of the post using rich text editor')

    meta_title = models.CharField(max_length=200, null=True, blank=True)

    meta_description = models.CharField(max_length=200, null=True, blank=True,
                                        help_text='It is recommended meta tag descriptions not to be longer than 160'
                                                  ' characters')

    meta_keywords = models.CharField(max_length=200, null=True, blank=True)

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the post')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created',
                                        help_text='Server date and time when the post was created')

    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified',
                                         help_text='Server date and time when the post was last modified')

    date_published = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                          verbose_name='Date published',
                                          help_text='Server date and time when the post was published')

    objects = PostManager()

    def save(self, *args, **kwargs):
        if self.date_published is None and self.status == self.STATUS.PUBLISHED:
            self.date_published = timezone.now()

        # Call the original save method of models.model
        super().save(*args, **kwargs)

    @property
    def number_of_words(self):
        return len(self.content.split())

    @property
    def reading_time_minutes(self):
        # return number of minutes to read the post, and round up to the nearest minute
        return ceil(self.number_of_words / 200)


@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        generated_slug = generate_unique_slug(instance, 'slug', 'title')
        instance.slug = generated_slug
