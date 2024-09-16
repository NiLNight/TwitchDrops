from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Password confirm')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password', ]

    username = forms.CharField()
    password = forms.CharField()

