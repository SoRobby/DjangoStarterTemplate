from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


# Backend classes
class CaseInsensitiveModelBackend(ModelBackend):
    """
    Backend class that authenticates using case-insensitive email field
    and case-sensitive password field.
    """

    def authenticate(
            self,
            request,
            username: Optional[str] = None,
            password: Optional[str] = None,
            **kwargs
    ) -> Optional[User]:
        """
        Authenticates the user based on the provided username (case-insensitive) and password.

        Args:
            request: The HTTP request object.
            username (str): The username (email) of the user.
            password (str): The password of the user.
            **kwargs: Additional keyword arguments.

        Returns:
            User: The authenticated user if successful, None otherwise.
        """
        account = get_user_model()

        if username is None:
            username = kwargs.get(account.USERNAME_FIELD)

        try:
            case_insensitive_username_field = '{}__iexact'.format(account.USERNAME_FIELD)
            user = account._default_manager.get(**{case_insensitive_username_field: username})
        except account.DoesNotExist:
            account().set_password(password)

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
