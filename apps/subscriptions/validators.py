from django.core.exceptions import ValidationError


def validate_features_list(value):
    if not isinstance(value, list):
        raise ValidationError('This field must be a list')
