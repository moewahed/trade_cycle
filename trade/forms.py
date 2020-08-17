from django import forms
from .models import Item, Review


class NewItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Item Name', 'autofocus': True})
        self.fields['desc'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Description'})
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = Item
        fields = ['name', 'desc', 'category']
