from django import forms
from .models import Blog, Comment


class NewPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control rounded-0', 'rows': 3})

    class Meta:
        model = Blog
        fields = ['content']


class NewCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = Comment
        fields = ['comment']
