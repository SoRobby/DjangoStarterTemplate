import os
from math import ceil
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_delete

from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from db.abstract_models import DateCreatedAndModified, DateDeleted
from libs.utils.utils import generate_unique_slug
from .managers import PostManager


# Create your models here.


def upload_to_featured_images(instance, filename):
    if filename:
        return os.path.join('blog', str(instance.uuid), 'featured-image', filename)
    else:
        return os.path.join('blog', str(instance.uuid), 'featured-image')


class Post(DateCreatedAndModified, DateDeleted):
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

    featured_image_raw = models.ImageField(upload_to=upload_to_featured_images, blank=True, null=True,
                                           help_text='Original unedited image of the post')

    featured_image = models.ImageField(upload_to=upload_to_featured_images, blank=True, null=True,
                                       help_text='Featured image of the post')

    featured_image_thumbnail = models.ImageField(upload_to=upload_to_featured_images, blank=True, null=True,
                                                 help_text='Featured image thumbnail of the post')

    meta_title = models.CharField(max_length=200, null=True, blank=True,
                                  help_text='Title that will appear in search engines and browser tab. Recommended\
                                  length is 50-60 characters')

    meta_description = models.CharField(max_length=200, null=True, blank=True,
                                        help_text='Summary of the post. Recommended length is 50-160 characters')

    meta_keywords = models.CharField(max_length=200, null=True, blank=True,
                                     help_text='Comma-separated keywords. Keywords that describe the post. Recommended\
                                     number of keywords is 3-8')

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

    date_published = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                          verbose_name='Date published',
                                          help_text='Server date and time when the item was published')

    objects = PostManager()

    def __str__(self) -> str:
        return f'{self.title} - {self.pk}'

    def save(self, *args, **kwargs):
        if self.title_has_changed and self.slug is None:
            self.slug = self.generate_slug()

        # Set the date_published
        if self.release_status == self.ReleaseStatus.PUBLISHED and self.date_published is None:
            self.date_published = timezone.now()

        # Set the date_deleted if the post is deleted
        if self.is_deleted and self.date_deleted is None:
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


class Comment(DateCreatedAndModified, DateDeleted):
    # TODO - might want to rename this to BlogComment to add clearitiy in the event other apps will also include
    # a model called Comment.

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment',
                             help_text='The post that the comment is related to')

    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='child_comments',
                                       help_text='The parent comment that this comment replied to')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='user_comment', help_text='User that made the comment')

    content = models.TextField(max_length=6000, blank=True, verbose_name='Content', help_text='Comment content')

    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_upvotes', blank=True,
                                     help_text='Users who have upvoted this comment')

    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_downvotes', blank=True,
                                       help_text='Users who have downvoted this comment')

    is_flagged = models.BooleanField(default=False, verbose_name='Is flagged',
                                     help_text='Has the comment been flagged as a potential problem?')

    is_edited = models.BooleanField(default=False, verbose_name='Is edited',
                                    help_text='Has the comment been edited by the user?')

    is_deleted = models.BooleanField(default=False, verbose_name='Is deleted',
                                     help_text='Has the comment been deleted by the user?')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the item')

    def __str__(self) -> str:
        return f'{self.post.title} - Comment {self.pk}'

    def save(self, *args, **kwargs):
        # Set the date_deleted if the comment is deleted
        if self.is_deleted and self.date_deleted is None:
            self.date_deleted = timezone.now()

        if self.parent_comment == self:
            raise ValidationError('A comment cannot be the parent of itself')

        # Call the original save method of models.model
        super().save(*args, **kwargs)

    def toggle_vote(self, user, vote_type):
        """
        Toggles user's vote on a comment.
        :param user: The user toggling the vote.
        :param vote_type: Should be 'upvote' or 'downvote'.
        :return: None
        """
        if vote_type == 'upvote':
            if user in self.downvotes.all():
                self.downvotes.remove(user)
            self.upvotes.add(user)
        elif vote_type == 'downvote':
            if user in self.upvotes.all():
                self.upvotes.remove(user)
            self.downvotes.add(user)


# TODO - Not sure if this pre-save is relevant anymore.
@receiver(pre_save, sender=Post)
def delete_old_files(sender, instance, **kwargs):
    """
    Delete old featured_image and featured_image_thumbnail files before saving the new ones.
    """

    # Get the existing Post object from the database, if available.
    if instance.pk:
        try:
            existing_post = Post.objects.get(pk=instance.pk)
        except Post.DoesNotExist:
            return  # No matching Post found, do nothing

        # Check if featured_image_raw has changed
        if instance.featured_image_raw and existing_post.featured_image_raw != instance.featured_image_raw:
            existing_file_path = os.path.join(settings.MEDIA_ROOT, str(existing_post.featured_image_raw))
            if os.path.isfile(existing_file_path):
                os.remove(existing_file_path)

        # Check if featured_image has changed
        if instance.featured_image and existing_post.featured_image != instance.featured_image:
            existing_file_path = os.path.join(settings.MEDIA_ROOT, str(existing_post.featured_image))
            if os.path.isfile(existing_file_path):
                os.remove(existing_file_path)

        # Check if featured_image_thumbnail has changed
        if instance.featured_image_raw and existing_post.featured_image_thumbnail != instance.featured_image_thumbnail:
            existing_thumbnail_path = os.path.join(settings.MEDIA_ROOT, str(existing_post.featured_image_thumbnail))
            if os.path.isfile(existing_thumbnail_path):
                os.remove(existing_thumbnail_path)


pre_save.connect(delete_old_files, sender=Post)


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    # Delete the featured_image_raw file
    if instance.featured_image_raw:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, instance.featured_image_raw.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, instance.featured_image_raw.path))

    # Delete the featured_image file
    if instance.featured_image:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, instance.featured_image.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, instance.featured_image.path))

    # Delete the featured_image_thumbnail file
    if instance.featured_image_thumbnail:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, instance.featured_image_thumbnail.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, instance.featured_image_thumbnail.path))

# @receiver(pre_save, sender=Post)
# def post_pre_save(sender, instance, *args, **kwargs):
#     if instance.slug is None:
#         generated_slug = generate_unique_slug(instance, 'slug', 'title')
#         instance.slug = generated_slug
#
#     print('PRE SAVE SIGNAL CALLED!!!!')
