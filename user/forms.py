from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import User


class NewUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'First Name', 'autofocus': True})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email', 'autofocus': False})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password Confirmation'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True,
                             widget=forms.EmailInput(attrs={
                                 'id': 'EmailInput',
                                 'class': 'form-control',
                                 'placeholder': 'Email',
                                 'required': 'required',
                                 'autofocus': True,
                             }))
    password = forms.CharField(strip=False, label='Password', required=True,
                               widget=forms.PasswordInput(attrs={
                                   'id': 'PasswordInput',
                                   'class': 'form-control',
                                   'placeholder': 'Password',
                                   'required': 'required',
                               }))
    error_messages = {
        'invalid_login': "Please enter a correct Email and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(email=email)
        except:
            user = None
        if user is None:
            raise forms.ValidationError('We can\'t found any user with that Email!')
        if not authenticate(email=email, password=password):
            if user is not None and user.is_active:
                raise forms.ValidationError('Email or Password is not correct please try again!')
            raise forms.ValidationError('User is not Activated please check you Email')


class AvatarChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = User
        fields = ['profile_pic']
        
        
class CoverChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cover_pic'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = User
        fields = ['cover_pic']
