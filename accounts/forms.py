from django import forms
from .models import User

class UserLoginform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email','password']
		widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control item', 'placeholder':'이메일'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control item', 'placeholder':'비밀번호'}),
        }

class UserSignupform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email','password','username']
		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control item', 'placeholder':'닉네임'}),
            'email': forms.EmailInput(attrs={'class': 'form-control item', 'placeholder':'이메일'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control item', 'placeholder':'비밀번호'}),
        }

# class smsform(forms.ModelForm):
# 	class Meta:
# 		model = User
# 		fields = ['phone_number','auth_number']
		
