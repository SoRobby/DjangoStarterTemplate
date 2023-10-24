import os
import shutil
from math import ceil
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from tinymce.models import HTMLField

from db.abstract_models import DateCreatedAndModified, DateDeleted
from libs.utils.utils import generate_unique_slug
from .managers import ArticleManager

User = settings.AUTH_USER_MODEL


def upload_to_featured_images(instance, filename):
    if filename:
        return os.path.join('blog', str(instance.uuid), 'featured-image', filename)
    else:
        return os.path.join('blog', str(instance.uuid), 'featured-image')


# Models
# class Category(DateCreatedAndModified):
#     name = models.CharField(max_length=200, unique=True, verbose_name='Name',
#                             help_text='Name of the category')
#     slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='Slug', help_text='The\
#                             URL slug based on the category name, slug fields should be 50 characters or less')
#     description = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Description',
#                                       help_text='Description of the category')
#     uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
#                             help_text='Unique identifier for the category')


class Article(DateCreatedAndModified, DateDeleted):
    FEATURED_IMAGE_ASPECT_RATIO = 16 / 9
    FEATURED_IMAGE_SIZE = (730, 428)
    FEATURED_IMAGE_THUMBNAIL_SIZE = (300, 300)

    class ReleaseStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        REVIEW = 'review', 'Review'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Private'

    title = models.CharField(max_length=200, help_text='The title of the article')

    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='Slug',
                            help_text='The URL slug based on the article title, slug fields should be 50 characters or\
                            less')

    lead_author = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='authored_articles_as_lead', verbose_name='Lead author',
                                    help_text='Lead author of the article')

    authors = models.ManyToManyField(User, related_name='authored_articles', help_text='Article authors')

    release_status = models.CharField(max_length=55, default=ReleaseStatus.DRAFT, choices=ReleaseStatus.choices,
                                      verbose_name='Release status',
                                      help_text='Current status of the article')

    visibility = models.CharField(max_length=55, default=Visibility.PUBLIC, choices=Visibility.choices,
                                  verbose_name='Visibility', help_text='Visibility of the article')

    content = HTMLField(blank=True, null=True, verbose_name='Content',
                        help_text='Primary content of the article using rich text editor')

    featured_image_raw = models.ImageField(upload_to=upload_to_featured_images, blank=True, null=True,
                                           verbose_name='Featured thumbnail raw',
                                           help_text='Original unedited image of the article')

    featured_image = models.ImageField(upload_to=upload_to_featured_images, blank=True, null=True,
                                       verbose_name='Featured thumbnail', help_text='Featured image of the article')

    featured_image_thumbnail = models.ImageField(upload_to=upload_to_featured_images, blank=True, null=True,
                                                 verbose_name='Featured thumbnail',
                                                 help_text='Featured image thumbnail of the article')

    number_of_revisions = models.PositiveIntegerField(default=0, verbose_name='Number of revisions',
                                                      help_text='Number of revisions that have been made to the\
                                                      article')

    meta_title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Meta title',
                                  help_text='Title that will appear in search engines and browser tab. Recommended\
                                  length is 50-60 characters')

    meta_description = models.CharField(max_length=200, null=True, blank=True,
                                        help_text='Summary of the article. Recommended length is 50-160 characters')

    meta_keywords = models.CharField(max_length=200, null=True, blank=True, verbose_name='Meta keywords',
                                     help_text='Comma-separated keywords. Keywords that describe the article.\
                                     Recommended number of keywords is 3-8')

    allow_comments = models.BooleanField(default=True, verbose_name='Allow comments',
                                         help_text='If checked, comments are allowed for this article')

    allow_sharing = models.BooleanField(default=True, verbose_name='Allow social media sharing',
                                        help_text='If checked, social media sharing is allowed for this article')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the article')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_articles',
                                   verbose_name='Created by', help_text='User who created the article')

    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_articles',
                                    verbose_name='Modified by', help_text='User who last modified the article')

    is_deleted = models.BooleanField(default=False, verbose_name='Is deleted',
                                     help_text='If checked, the article is deleted')

    deleted_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='deleted_articles', verbose_name='Deleted by',
                                   help_text='User who deleted the article')

    date_published = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                          verbose_name='Date published',
                                          help_text='Server date and time when the item was published')

    objects = ArticleManager()

    class Meta:
        ordering = ['-date_published', '-date_created']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self) -> str:
        return f'{self.pk} - {self.title}'

    def save(self, *args, **kwargs):
        if self.title_has_changed and self.slug is None:
            self.slug = self.generate_slug()

        # Set the date_published
        if self.release_status == self.ReleaseStatus.PUBLISHED and self.date_published is None:
            print('SETTING DATE PUBLISHED')
            self.date_published = timezone.now()
        elif self.release_status != self.ReleaseStatus.PUBLISHED and self.date_published is not None:
            self.date_published = None

        # Set the date_deleted if the article is deleted
        if self.is_deleted and self.date_deleted is None:
            self.date_deleted = timezone.now()
        else:
            self.date_deleted = None
            self.is_deleted = False

        self.number_of_revisions += 1

        # Call the original save method of models.model
        super().save(*args, **kwargs)

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

    def title_has_changed(self):
        # Check if the title has changed and needs a new slug
        try:
            orig = Article.objects.get(pk=self.pk)
            return orig.title != self.title
        except Article.DoesNotExist:
            return True

    def generate_slug(self):
        new_slug = slugify(self.title)
        qs_exists = Article.objects.filter(slug=new_slug).exclude(id=self.id).exists()

        if qs_exists:
            new_slug = f'{new_slug}-{timezone.now().strftime("%Y-%m-%d")}'
            qs_exists = Article.objects.filter(slug=new_slug).exclude(id=self.id).exists()

        if qs_exists:
            new_slug = generate_unique_slug(self, 'slug', 'title')

        return new_slug

    @staticmethod
    def get_release_status_choices_as_dict():
        return dict(Article.ReleaseStatus.choices)

    @staticmethod
    def get_release_status_choices_as_list():
        """
        Returns the release status choices as a list of dictionaries with keys 'key' and 'name' for each choice.
        :return: list of dictionaries
        """
        return [{'key': key, 'name': name} for key, name in Article.ReleaseStatus.choices]

    @staticmethod
    def get_visibility_choices_as_dict():
        return dict(Article.Visibility.choices)

    @staticmethod
    def get_visibility_choices_as_list():
        """
        Returns the release status choices as a list of dictionaries with keys 'key' and 'name' for each choice.
        :return: list of dictionaries
        """
        return [{'key': key, 'name': name} for key, name in Article.Visibility.choices]


class Comment(DateCreatedAndModified, DateDeleted):
    # TODO - might want to rename this to ArticleComment to add clarity in the event other apps will also include
    # a model called Comment.

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment',
                                verbose_name='Article', help_text='The article that the comment is related to')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_comment',
                             verbose_name='User', help_text='User that made the comment')

    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='child_comments', verbose_name='Parent comment',
                                       help_text='The parent comment that this comment replied to')

    content = models.TextField(max_length=6000, blank=True, verbose_name='Content', help_text='Comment content')

    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True, verbose_name='Likes',
                                   help_text='Users who have liked this comment')

    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True, verbose_name='Dislikes',
                                      help_text='Users who have disliked this comment')

    is_flagged = models.BooleanField(default=False, verbose_name='Is flagged',
                                     help_text='Has the comment been flagged as a potential problem?')

    is_edited = models.BooleanField(default=False, verbose_name='Is edited',
                                    help_text='Has the comment been edited by the user?')

    is_deleted = models.BooleanField(default=False, verbose_name='Is deleted',
                                     help_text='Has the comment been deleted by the user?')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the item')

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self) -> str:
        return f'Comment {self.pk}'

    def save(self, *args, **kwargs):
        # Set the date_deleted if the comment is deleted
        if self.is_deleted and self.date_deleted is None:
            self.date_deleted = timezone.now()

        if self.parent_comment == self:
            raise ValidationError('A comment cannot be the parent of itself')

        # Call the original save method of models.model
        super().save(*args, **kwargs)

    @property
    def number_of_likes(self):
        return self.likes.count()

    @property
    def number_of_dislikes(self):
        return self.dislikes.count()


@receiver(pre_save, sender=Article)
def delete_old_files(sender, instance, **kwargs):
    """
    Delete old featured_image and featured_image_thumbnail files before saving the new ones.
    """

    # Get the existing Post object from the database, if available.
    if instance.pk:
        try:
            existing_article = Article.objects.get(pk=instance.pk)
        except Article.DoesNotExist:
            return  # No matching Post found, do nothing

        # Check if featured_image_raw has changed
        if instance.featured_image_raw and existing_article.featured_image_raw != instance.featured_image_raw:
            existing_file_path = os.path.join(settings.MEDIA_ROOT, str(existing_article.featured_image_raw))
            if os.path.isfile(existing_file_path):
                os.remove(existing_file_path)

        # Check if featured_image has changed
        if instance.featured_image and existing_article.featured_image != instance.featured_image:
            existing_file_path = os.path.join(settings.MEDIA_ROOT, str(existing_article.featured_image))
            if os.path.isfile(existing_file_path):
                os.remove(existing_file_path)

        # Check if featured_image_thumbnail has changed
        if instance.featured_image_raw and existing_article.featured_image_thumbnail != instance.featured_image_thumbnail:
            existing_thumbnail_path = os.path.join(settings.MEDIA_ROOT, str(existing_article.featured_image_thumbnail))
            if os.path.isfile(existing_thumbnail_path):
                os.remove(existing_thumbnail_path)


@receiver(post_delete, sender=Article)
def article_delete_files(sender, instance, **kwargs):
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

    # Delete content associated with the article
    content_directory = os.path.join(settings.MEDIA_ROOT, f'blog/{instance.uuid}/content')
    if os.path.exists(content_directory):
        shutil.rmtree(content_directory)

    # # Find all files in the path of blog/<article_uuid>/content and delete all data
    # if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'blog', str(instance.uuid), 'content')):
    #     for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, 'blog', str(instance.uuid), 'content')):
    #         file_path = os.path.join(settings.MEDIA_ROOT, 'blog', str(instance.uuid), 'content', filename)
    #         try:
    #             if os.path.isfile(file_path) or os.path.islink(file_path):
    #                 os.unlink(file_path)
    #         except Exception as e:
    #             print('Failed to delete %s. Reason: %s' % (file_path, e))
