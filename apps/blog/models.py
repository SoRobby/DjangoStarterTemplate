from math import ceil
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from libs.utils.utils import generate_unique_slug
from .managers import PostManager


# Create your models here.


class Post(models.Model):
    class ReleaseStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        REVIEW = 'review', 'Review'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=200, help_text='The title of the post')

    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True,
                            help_text='The URL slug based on the post title, slug fields should be 50 characters or\
                            less')

    lead_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='authored_posts_as_lead',
                                    help_text='Lead author of the post')

    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='authored_posts', help_text='Post authors.')

    release_status = models.CharField(max_length=55, default=ReleaseStatus.DRAFT, choices=ReleaseStatus.choices,
                                      verbose_name='Release status',
                                      help_text='Current status of the post')

    content = CKEditor5Field(config_name='extends', verbose_name='Content',
                             help_text='Primary content of the post using rich text editor')

    featured_image = models.ImageField(upload_to='blog/featured-images/', blank=True, null=True,
                                       help_text='Featured image of the post')

    meta_title = models.CharField(max_length=200, null=True, blank=True,
                                  help_text='Title that will appear in search engines and browser tab. Recommended\
                                  length is 50-60 characters.')

    meta_description = models.CharField(max_length=200, null=True, blank=True,
                                        help_text='Summary of the post. Recommended length is 50-160 characters.')

    meta_keywords = models.CharField(max_length=200, null=True, blank=True,
                                     help_text='Comma-separated keywords. Keywords that describe the post. Recommended\
                                     number of keywords is 3-8.')

    allow_comments = models.BooleanField(default=True, verbose_name='Allow comments',
                                         help_text='If checked, comments are allowed for this post')

    allow_sharing = models.BooleanField(default=True, verbose_name='Allow social media sharing',
                                        help_text='If checked, social media sharing is allowed for this post')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the post')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_posts',
                                   help_text='User who created the post')

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='modified_posts',
                                    help_text='User who last modified the post')

    is_deleted = models.BooleanField(default=False, verbose_name='Is deleted',
                                     help_text='If checked, the post is deleted')

    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='deleted_posts', help_text='User who deleted the post')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created',
                                        help_text='Server date and time when the post was created')

    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified',
                                         help_text='Server date and time when the post was last modified')

    date_published = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                          verbose_name='Date published',
                                          help_text='Server date and time when the post was published')

    date_deleted = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                        verbose_name='Date deleted',
                                        help_text='Server date and time when the post was deleted')

    objects = PostManager()

    def save(self, *args, **kwargs):
        print('blog models.py save() called')
        if self.slug is None or self.title_has_changed:
            self.slug = self.generate_slug()

        # Set the date_published
        if self.date_published is None and self.release_status == self.ReleaseStatus.PUBLISHED:
            self.date_published = timezone.now()

        # Set the date_deleted if the post is deleted
        if self.date_deleted is None and self.is_deleted:
            self.date_deleted = timezone.now()

        # Call the original save method of models.model
        super().save(*args, **kwargs)

    def title_has_changed(self):
        # Check if the title has changed and needs a new slug
        try:
            orig = Post.objects.get(pk=self.pk)
            return orig.title != self.title
        except Post.DoesNotExist:
            return True

    def generate_slug(self):
        new_slug = slugify(self.title)
        qs_exists = Post.objects.filter(slug=new_slug).exclude(id=self.id).exists()

        if qs_exists:
            new_slug = f'{new_slug}-{timezone.now().strftime("%Y-%m-%d")}'
            qs_exists = Post.objects.filter(slug=new_slug).exclude(id=self.id).exists()

        if qs_exists:
            new_slug = generate_unique_slug(self, 'slug', 'title')

        return new_slug

    @property
    def number_of_words(self):
        return len(self.content.split())

    @property
    def reading_time_minutes(self):
        # return number of minutes to read the post, and round up to the nearest minute
        return ceil(self.number_of_words / 200)

    @property
    def keywords_list(self):
        return self.meta_keywords.split(',')

    @staticmethod
    def get_release_status_choices_as_dict():
        return dict(Post.ReleaseStatus.choices)

    @staticmethod
    def get_release_status_choices_as_list():
        """
        Returns the release status choices as a list of dictionaries with keys 'key' and 'name' for each choice.
        :return: list of dictionaries
        """
        return [{'key': key, 'name': name} for key, name in Post.ReleaseStatus.choices]

# @receiver(pre_save, sender=Post)
# def post_pre_save(sender, instance, *args, **kwargs):
#     if instance.slug is None:
#         generated_slug = generate_unique_slug(instance, 'slug', 'title')
#         instance.slug = generated_slug
#
#     print('PRE SAVE SIGNAL CALLED!!!!')
