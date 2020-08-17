from django import forms
from .models import BlogImage, CommentImage, ItemImage, ReviewImage


class BlogImageNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['image'].required = False

    class Meta:
        model = BlogImage
        fields = ['image']


class CommentImageNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control', 'required': False})
        self.fields['image'].required = False

    class Meta:
        model = CommentImage
        fields = ['image']


class ItemImageNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control', 'required': False})
        self.fields['image'].required = False

    class Meta:
        model = ItemImage
        fields = ['image']


class ReviewImageNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control', 'required': False})
        self.fields['image'].required = False

    class Meta:
        model = ReviewImage
        fields = ['image']
