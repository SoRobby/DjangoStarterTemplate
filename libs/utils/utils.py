import inspect
import logging
from uuid import uuid4

from django.core.files.storage import default_storage
from django.db.models import Model
from django.utils.encoding import force_str
from django.utils.text import slugify





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
