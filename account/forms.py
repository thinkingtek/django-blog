from django import forms
from .models import Profile, User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm


class UserRegForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Stay logged in ?')

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'remember_me')

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = 'Email | Username'


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


class PasswordFormReset(PasswordResetForm):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(
        attrs={'placeholder': 'Enter Email'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            email_check = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Email Address cannot be used.')
        return email


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': "Firstname"
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': "Lastname"
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Your Email Address"
    }))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Email subject"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Type in your message"
    }))
