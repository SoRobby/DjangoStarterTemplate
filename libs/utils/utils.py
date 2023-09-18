from uuid import uuid4

from django.contrib import messages
from django.db.models import Model
from django.utils.encoding import force_str
from django.utils.text import slugify


def send_notification(request, tag: str, title: str = '', message: str = '') -> None:
    """
    Adds a formatted message to the Django messages framework based on the provided tag.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        tag (str): The tag that determines the message level. Valid options are 'info', 'success', 'warning', 'error'.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    message_levels = {
        'info': messages.INFO,
        'success': messages.SUCCESS,
        'warning': messages.WARNING,
        'error': messages.ERROR,
    }
    level = message_levels.get(tag, None)
    messages.add_message(request, level=level, message=message, extra_tags=title)


def generate_unique_slug(instance: Model, slug_target_field: str, slug_source_field: str,
                         max_iterations: int = 200) -> str:
    """
    Generate a unique slug for a Django model instance.

    Parameters:
    instance (Model): Instance of the Django model.
    slug_source_field (str): Field name of the instance to base the slug on.
    slug_target_field (str): Field name where the unique slug will be stored.
    max_iterations (int, default=200): Maximum number of iterations to try generating a unique slug.

    Returns:
    str: Unique slug string for the instance.

    Raises:
    ValueError: If a unique slug cannot be generated within max_iterations.
    """

    slug = slugify(getattr(instance, slug_source_field))

    InstanceClass = instance.__class__

    for num in range(1, max_iterations + 1):
        qs = InstanceClass.objects.filter(**{slug_target_field: slug}).exclude(id=instance.id)

        if not qs.exists():
            return slug

        uuid = force_str(uuid4()).replace('-', '')[:6].lower()
        slug = f'{slug}-{uuid}'

    raise ValueError(f"Could not generate a unique slug for {instance} after {max_iterations} tries")


def get_model_lengths(model_class):
    field_lengths = {}
    for field in model_class._meta.fields:
        field_info = {}

        # Check for max_length attribute and add to dictionary if exists
        if hasattr(field, 'max_length') and field.max_length is not None:
            field_info['max_length'] = field.max_length

        # Check for min_length attribute and add to dictionary if exists
        # Note: min_length is not a built-in Django model field option for models.CharField, but it is for forms.CharField.
        # If you've customly added a 'min_length' attribute, this will catch it.
        if hasattr(field, 'min_length') and field.min_length is not None:
            field_info['min_length'] = field.min_length

        if field_info:
            field_lengths[field.name] = field_info

    return field_lengths