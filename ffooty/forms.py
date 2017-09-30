from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'type': 'username', 'placeholder': 'Username', 'class': 'form-control', 'required': '', 'autofocus': ''}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'Password', 'class': 'form-control', 'required': ''}))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(self, request, *args, **kwargs)
        
        
class PasswordChangeForm(AuthenticationForm):
    old_password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'Old Password', 'class': 'form-control', 'required': ''}))
    new_password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'New Password', 'class': 'form-control', 'required': ''}))
    new_password2 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'Confirm New Password', 'class': 'form-control', 'required': ''}))

    def __init__(self, request=None, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(self, request, *args, **kwargs)


class AuctionFileUploadForm(forms.Form):
    """
    Form for uploading a csv file of auction outcomes.
    """
    file = forms.FileField(label='File')
    initialise = forms.BooleanField(label='Initialise')


class PlayerFileUploadForm(forms.Form):
    """
    Form for uploading an html file of player scores.
    """
    file = forms.FileField(label='File')
