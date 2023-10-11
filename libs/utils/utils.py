from datetime import datetime
from io import BytesIO
from uuid import uuid4
import inspect
import logging

from PIL import Image
from django.contrib import messages
from django.core.files import File
from django.core.files.storage import default_storage
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


def send_info_notification(request, title: str = '', message: str = '') -> None:
    """
    Adds an info message to the Django messages framework.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    send_notification(request, tag='info', title=title, message=message)


def send_success_notification(request, title: str = '', message: str = '') -> None:
    """
    Adds a success message to the Django messages framework.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    send_notification(request, tag='success', title=title, message=message)


def send_warning_notification(request, title: str = '', message: str = '') -> None:
    """
    Adds a warning message to the Django messages framework.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    send_notification(request, tag='warning', title=title, message=message)


def send_error_notification(request, title: str = '', message: str = '') -> None:
    """
    Adds an error message to the Django messages framework.

    Args:
        request (HttpRequest): The HTTP request object to which the message will be added.
        title (str, optional): The title of the message. Defaults to an empty string.
        message (str, optional): The content of the message. Defaults to an empty string.

    Returns:
        None

    Raises:
        None
    """

    send_notification(request, tag='error', title=title, message=message)


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


def process_image(image, crop_dimensions=None, resize_dimensions=None, file_format=None):
    """
    Process an image by cropping and resizing it. Optionally set the file format.

    Parameters:
    - image (PIL.Image): The original image.
    - crop_dimensions (tuple, optional): The x, y, width, and height to crop the image. Default is None.
    - resize_dimensions (tuple, optional): The new width and height to resize the image. Default is None.
    - file_format (str, optional): The desired file format ('png', 'jpeg', etc.). Default is None.

    Returns:
    - django.core.files.File: Processed image file.
    """

    # If resize_dimensions is provided, perform cropping and resizing
    if resize_dimensions:
        # Extract x, y, width, and height from crop_dimensions
        x, y, width, height = crop_dimensions

        # Crop the image based on provided dimensions
        image = image.crop((x, y, x + width, y + height))

        # Resize the image based on provided dimensions
        image = image.resize(resize_dimensions, Image.LANCZOS)

    # If no file_format is provided, use the format of the original image
    if file_format is None:
        file_format = image.format

    # Convert PIL image to BytesIO
    image_io = BytesIO()

    # Save the PIL image in BytesIO object, using the provided or original format
    image.save(image_io, format=file_format)

    # Return the BytesIO object as a Django File object
    return File(image_io)


def save_file_to_field(model_instance, field_name, file, directory_path, file_name=None):
    """
    Save a file to a specific field on a model instance, replacing the old file if it exists.

    Parameters:
    - model_instance: Django model instance where the file will be saved.
    - field_name (str): The name of the field where the file will be saved.
    - file (File): The file to save.
    - directory_path (str): The directory where the file should be saved.
    - file_name (str, optional): The name to save the file as. If None, uses the existing filename.
    """
    if file_name is None:
        file_name = file.name

    # Create the full path for the file
    file_path = f"{directory_path}/{file_name}"

    # Delete the old file if it exists
    old_file_path = getattr(model_instance, field_name).path if getattr(model_instance, field_name) else None
    if old_file_path and default_storage.exists(old_file_path):
        default_storage.delete(old_file_path)

    # Save the new file
    default_storage.save(file_path, file)

    # Update the model field with the new file path
    setattr(model_instance, field_name, file_path)
    model_instance.save()


def log_view_call():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])

    if "self" in frame.frame.f_locals:
        cls = frame.frame.f_locals["self"].__class__
        caller_name = f"{cls.__name__}.{frame.function}"
    else:
        caller_name = frame.function

    module_name = module.__name__.split('.')[-2] if module else 'unknown'
    logging.debug(f'[{module_name.upper()}.{caller_name.upper()}] Called')
