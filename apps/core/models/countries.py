from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from apps.core.models import BaseModel


# Models
class Country(BaseModel):
    """
    Represents a country with essential details.

    Attributes:
    - name (CharField): The official name of the country.
    - slug (SlugField): A slug field version of the country's name.
    - country_code (CharField): The standard code representation of the country (e.g., "US" for the United States,
    "UK" for the United Kingdom).
    - phone_code (IntegerField): The international phone code associated with the country (e.g., 1 for the US, 44 for
    the UK).
    - flag (ImageField): An image representing the flag of the country.

    Meta:
    - ordering: Specifies the default ordering for the country, which is based on its name.
    - verbose_name: Human-readable singular form of the object.
    - verbose_name_plural: Human-readable plural form of the object.

    Methods:
    - __str__(): Returns a string representation of the country in the format: "Name (Country Code)".
    """
    name = models.CharField(max_length=255, verbose_name='Name', help_text='Name of the country')

    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug',
                            help_text='The slug based on the country name')

    country_code = models.CharField(max_length=16, verbose_name='Country code',
                                    help_text='Code of the country (e.g., US, UK, etc...)')

    phone_code = models.IntegerField(verbose_name='Phone code',
                                     help_text='Phone code of the country (e.g., 1, 44, etc...)')

    flag = models.ImageField(upload_to='flags', verbose_name='Flag', help_text='Flag of the country')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return f'{self.name} ({self.country_code})'


@receiver(pre_save, sender=Country)
def set_slug(sender, instance, *args, **kwargs):
    # Update the slug if the object is new or the object's name field has changed.
    if not instance.pk or (instance.pk and Country.objects.get(pk=instance.pk).name != instance.name):
        instance.slug = slugify(instance.name)
