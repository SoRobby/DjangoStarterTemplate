from django.contrib.auth.models import BaseUserManager


# Managers
class AccountManager(BaseUserManager):
    """
    Handles database operations for models in the accounts app.
    """

    def create_user(self, email, username, password=None):
        """
        Manages the process of creating a regular user.

        Parameters:
        email (str): User's email address. Must be unique.
        username (str): User's username. Must be unique.
        password (str, optional): User's password. Defaults to None.

        Returns:
        user: The created User instance.

        Raises:
        ValueError: If email or username is not provided.
        """
        # Check if email and username are provided
        if not email:
            raise ValueError('Users must have an email address.')
        if not username:
            raise ValueError('Users must have a username.')

        # Create the user
        # `self.model` is a reference to the model class that this manager is for.
        # `self.normalize_email(email)` normalizes the email by lowercasing the domain part of it
        user = self.model(email=self.normalize_email(email), username=username)

        # Set the user's password. This properly hashes the password.
        user.set_password(password)

        # Save the user object to the database
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """
        Manages the process of creating a superuser.

        Parameters:
        email (str): Superuser's email address. Must be unique.
        username (str): Superuser's username. Must be unique.
        password (str): Superuser's password.

        Returns:
        user: The created User instance with superuser privileges.
        """
        # Create the user using the `create_user` method
        user = self.create_user(email, username, password)

        # Assign superuser privileges to the user
        user.is_staff = True  # Staff status allows access to the admin site.
        user.is_admin = True  # Here, is_admin might be used for determining the user's admin status.
        user.is_superuser = True  # Superuser status provides all permissions automatically.

        # Save the user object to the database
        user.save(using=self._db)

        return user
