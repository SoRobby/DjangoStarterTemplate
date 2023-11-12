from uuid import uuid4

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
