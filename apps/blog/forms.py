from django import forms

from apps.accounts.models import Account
from .models import Post


class PostForm(forms.ModelForm):
    lead_author_email = forms.EmailField(label="Lead Author's Email", required=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'release_status', 'allow_comments', 'allow_sharing',
                  'meta_title', 'meta_description', 'meta_keywords']

    def save(self, commit=True):
        # Call the parent class's save method and get the Post object
        instance = super().save(commit=False)

        # Try to get the lead author by email
        lead_author_email = self.cleaned_data['lead_author_email']
        instance.lead_author = Account.objects.get(email=lead_author_email)

        # try:
        #     user = Account.objects.get(email=lead_author_email)
        #     instance.lead_author = user
        # except Account.DoesNotExist:
        #     print('User does not exist')

        # Save the instance if commit is True
        if commit:
            instance.save()

        return instance

