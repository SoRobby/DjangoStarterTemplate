import re

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import AccountSettings

# Use the get_user_model function to get the custom user model
Account = get_user_model()


class AccountAuthenticationForm(forms.ModelForm):
    """
    Form used to check if the email and password are valid and match.

    Notes:
        - Email is converted to lowercase before being checked
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        """
        Validates the form data by checking if the email and password are valid and match.

        Raises:
            forms.ValidationError: If the login is invalid.

        Returns:
            None
        """
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            password = self.cleaned_data['password']

            # Use the `authenticate` function to verify the email and password
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid login')


class RegistrationForm(UserCreationForm):
    """
    Form for user registration, extending the built-in UserCreationForm.

    Fields:
        - email: Required email field.
        - username: Required username field with specific length and character restrictions.
        - name: Optional name field.

    Form Validation Functions:
        - clean_email: Validates the email field for uniqueness.
        - clean_username: Validates the username field for length, alphanumeric characters, and uniqueness.
    """
    email = forms.EmailField(
        required=True,
        max_length=255,
        help_text="Required. Add a valid email address."
    )

    username = forms.CharField(required=True, min_length=4, max_length=16,
                               error_messages={
                                   'required': 'Enter a valid username.',
                                   'min_length': 'Usernames must be between 4 and 16 characters long.',
                                   'max_length': 'Usernames must be between 4 and 16 characters long.'
                               })

    name = forms.CharField(required=False, max_length=120)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', 'name')

    # Form validation functions
    def clean_email(self):
        """
        Validates the email field for uniqueness.

        Returns:
            str: The cleaned and lowercase email value if it's unique.

        Raises:
            forms.ValidationError: If the email is already registered.
        """
        email = self.cleaned_data['email'].lower()

        # Check to make sure email is unique
        try:
            Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} is unavailable.')

    def clean_username(self):
        """
        Validates the username field for length, alphanumeric characters, and uniqueness.

        Returns:
            str: The cleaned and lowercase username value if it's unique and meets the criteria.

        Raises:
            forms.ValidationError: If the username is invalid or already taken.
        """
        username = self.cleaned_data['username'].lower()

        # Check to make sure username is the correct length
        if len(username) < 4 or len(username) > 16:
            raise forms.ValidationError('Usernames must be between 4 and 16 characters long.')

        # Check to make sure username is alphanumeric
        if re.match(r'^[a-zA-Z0-9_]*$', username) != None:
            try:
                Account.objects.get(username=username)
            except Exception as e:
                return username
            raise forms.ValidationError(f'Username "{username}" is unavailable.')
        else:
            raise forms.ValidationError(f'Usernames must only contain alphanumeric characters.')


class AccountSettingsForm(forms.ModelForm):
    """

    """

    class Meta:
        model = AccountSettings
        fields = ('receive_marketing_emails', 'receive_weekly_digest_emails', 'receive_discovery_emails',
                  'receive_site_update_emails', 'receive_inbox_message_notifications',
                  'receive_announcement_notifications')
