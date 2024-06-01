from typing import Any
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.widgets import PasswordInput, TextInput
# from .models import User

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate', 'placeholder':'+998123456789'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class UserCreateForm(forms.ModelForm):
    first_name = forms.CharField(widget=TextInput(attrs={'placeholder':'First name'}), required=True)
    last_name = forms.CharField(widget=TextInput(attrs={'placeholder':'Last name'}), required=True)
    username = forms.CharField(widget=TextInput(attrs={'placeholder':'+998123456789'}), required=True)
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}), required=True)
    confirm_password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Confirm password'}), required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("bu telefon raqam bilan foydalanuvchi ro'yxatdan o'tgan")
        
        return username
    
    def clean_confirm_password(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError("parollar bir biriga teng bo'lishi kk")
        return data['confirm_password']
    
    def save(self, commit = True) -> Any:
        user = super().save(commit)
        user.set_password(self.cleaned_data['confirm_password'])
        user.save()
        return user
