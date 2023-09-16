from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'lead_author', 'allow_comments'
        ]
        # fields = [
        #     'title', 'content', 'lead_author', 'authors', 'release_status', 'content', 'meta_title', 'meta_description',
        #     'meta_keywords', 'allow_comments', 'allow_sharing', 'created_by', 'modified_by'
        # ]

        lead_author = forms.EmailField()

        def clean_allow_comments(self):
            print('CLEANING FORM!!!')
            allow_comments = self.cleaned_data.get('allow_comments')
            if allow_comments not in [True, False]:
                raise forms.ValidationError("Invalid value for allow_comments")
            return allow_comments