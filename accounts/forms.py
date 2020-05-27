from django.forms import ModelForm
from .models import *
from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'
		exclude=['user']
		widgets = {'image': forms.FileInput}



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2","first_name","last_name")



    def clean_email(self):
        data = self.cleaned_data["email"]
        try:
            user_email = User.objects.get(email=data)
        except User.DoesNotExist:
            return data
        else:
            raise forms.ValidationError("Email already exist")
        
    def clean_username(self):
        datas = self.cleaned_data["username"]
        try:
            user_username = User.objects.get(username=datas)
        except User.DoesNotExist:
            return datas
        else:
            raise forms.ValidationError("username already exist")

    