from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'release_status', 'allow_comments', 'allow_sharing',
                  'meta_title', 'meta_description', 'meta_keywords']

        lead_author = forms.EmailField()


        # def __init__(self, *args, **kwargs):
        #     super(My_Form, self).__init__(*args, **kwargs)
        #     self.fields['address'].required = False

        # def clean_allow_comments(self):
        #     allow_comments = self.cleaned_data.get('allow_comments')
        #     if allow_comments not in [True, False]:
        #         raise forms.ValidationError("Invalid value for allow_comments")
        #     return allow_comments