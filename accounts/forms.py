from django import forms
from django.contrib.auth import authenticate,get_user_model
from .models import Profile

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    pwrd1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    pwrd2 = forms.CharField(label='Password Confirm',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs:
            raise forms.ValidationError('Sorry.This email is already taken!')
        return email

    def clean_pwrd2(self):
        pwrd1 = self.cleaned_data.get('pwrd1')
        pwrd2 = self.cleaned_data.get('pwrd2')
        if pwrd1 and pwrd2 and pwrd1!=pwrd2:
            raise forms.ValidationError('Passwords Must Match!')
        return pwrd2


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image','dob')
