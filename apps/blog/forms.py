from django import forms
from django.conf import settings
from tinymce.widgets import TinyMCE

from apps.accounts.models import Account
from .models import Article


class ArticleForm(forms.ModelForm):
    lead_author_email = forms.EmailField(label="Lead Author's Email", required=True)
    save_type = forms.CharField(required=False)

    class Meta:
        model = Article
        fields = ['title', 'release_status', 'visibility', 'allow_comments', 'content', 'allow_sharing',
                  'meta_title', 'meta_description', 'meta_keywords']
        widgets = {
            'content': TinyMCE(mce_attrs=settings.TINYMCE_BLOG_ARTICLE_CONFIG),
        }

    def save(self, commit=True):
        # Call the parent class's save method and get the Post object
        instance = super().save(commit=False)

        print(self.cleaned_data)

        # Try to get the lead author by email
        lead_author_email = self.cleaned_data['lead_author_email']
        instance.lead_author = Account.objects.get(email=lead_author_email)

        # Handle logic for save_type
        save_type = self.cleaned_data['save_type']
        if save_type == 'publish':
            instance.release_status = 'published'

        elif save_type == 'draft':
            instance.release_status = 'draft'




        # Save the instance if commit is True
        if commit:
            instance.save()

        return instance
