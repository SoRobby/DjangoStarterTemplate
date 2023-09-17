from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    FeedbackForm is a ModelForm subclass that handles the creation and updating
    of Feedback objects. This form is specifically designed for handling user
    feedback about a web page.

    Attributes:
        model (Model): The model class (`Feedback`) this form is linked to.
        fields (list): List of field names that will be displayed in the form and
                       used in the creation or updating of the object.

    Methods:
        save: Overrides the save method of ModelForm to include user-specific
              data if the user is authenticated.
    """

    class Meta:
        model = Feedback
        fields = ['content', 'page_url']

    def save(self, user=None):
        """
        Save the form instance.

        This method overrides the parent class's save method. If the user is authenticated,
        it populates additional fields (`user`, `name`, and `email`) in the Feedback instance.

        Parameters:
            user (User, optional): The user instance, if the user is authenticated.
                                    Defaults to None.

        Returns:
            Feedback: The saved Feedback model instance.
        """
        instance = super().save(commit=False)
        if user and user.is_authenticated:
            instance.user = user
            instance.name = user.name
            instance.email = user.email

        instance.save()
        return instance
