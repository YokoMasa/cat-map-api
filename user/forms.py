from django import forms
  
from .models import User

class TwitterLoginForm(forms.Form):
  access_token_key = forms.CharField()
  access_token_secret = forms.CharField()

class GoogleLoginForm(forms.Form):
  auth_code = forms.CharField()