from uuid import uuid4

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.accounts.models import Account


class ProfileEditGeneralForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'description', 'theme', 'is_profile_public', 'profile_image')


class ChangeEmailForm(forms.Form):
    """
    Django Form to handle change of user email.

    Attributes:
    email (forms.EmailField): Django form field for email.

    Methods:
    clean_email(): Check if the email is already in use.
    save(user: Type[get_user_model()]): Change user's email, mark it as unverified, generate a new token and save the
    user instance.
    """

    email = forms.EmailField(max_length=255)

    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Email is already in use")
        return email

    def save(self, user) -> None:
        """
        Save the form's email to the user instance, mark the email as unverified, generate a new token and save the
        user instance.

        Parameters:
        user (Type[get_user_model()]): An instance of the User model.

        Returns:
        None
        """

        user.email = self.cleaned_data.get('email')
        user.email_verified = False
        user.email_verification_token = uuid4()
        user.save()


class SupportMessageForm(forms.Form):
    """
    Form for sending a support message.

    Attributes:
    name (forms.CharField): Sender's name.
    email (forms.EmailField): Sender's email.
    subject (forms.CharField): Subject of the message.
    message (forms.CharField): The message body.
    """

    name = forms.CharField(max_length=120)
    email = forms.EmailField(max_length=255)
    subject = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea)

    def clean_name(self) -> str:
        return self.cleaned_data.get('name')

    def clean_email(self) -> str:
        return self.cleaned_data.get('email')

    def clean_subject(self) -> str:
        return self.cleaned_data.get('subject')

    def clean_message(self) -> str:
        return self.cleaned_data.get('message')
