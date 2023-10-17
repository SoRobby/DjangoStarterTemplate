from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


# Models
class Country(models.Model):
    name = models.CharField(max_length=255, help_text='Name of the country')

    slug = models.SlugField(max_length=255, unique=True, help_text='The slug based on the country name')

    country_code = models.CharField(max_length=16, help_text='Code of the country (e.g., US, UK, etc.)')

    phone_code = models.IntegerField(validators=[MinValueValidator(0)],
                                     help_text='Phone code of the country (e.g., 1, 44, etc.)')

    flag = models.ImageField(upload_to='flags', help_text='Flag of the country')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the country')

    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created',
                                        help_text='Server date and time when the country was created')

    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified',
                                         help_text='Server date and time when country was last modified')

    def __str__(self):
        return f'{self.name} ({self.country_code})'

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ('name',)


@receiver(pre_save, sender=Country)
def set_slug(sender, instance, *args, **kwargs):
    # Update the slug if the object is new or the name has changed.
    if not instance.pk or (instance.pk and Country.objects.get(pk=instance.pk).name != instance.name):
        instance.slug = slugify(instance.name)
