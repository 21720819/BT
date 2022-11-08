from wsgiref.validate import validator
from django import forms
from .models import User
from .validators import validate_symbols
from django.contrib.auth.forms import SetPasswordForm

class CustomPasswordSetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class':
            'form-control',
        })
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class':
            'form-control',
        })
        self.fields['new_password2'].help_text = None

class UserLoginform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email','password']
		widgets = {
            'email': forms.EmailInput(  attrs={'class': 'form-control item', 'placeholder':'이메일'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control item', 'placeholder':'비밀번호'}),
        }
		# def clean_email(self):
		# 	email = self.clean_data['email']
		# 	if ("@ynu.ac.kr" not in email):
		# 		raise ValidationError("영남대학교 이메일을 사용해야합니다.")
		# 	return email
        

class UserSignupform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email','password','username']
		email = forms.CharField(max_length=80, validators=[validate_symbols])
		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control item', 'placeholder':'닉네임'}),
            'email': forms.EmailInput(attrs={'class': 'form-control item', 'placeholder':'이메일'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control item', 'placeholder':'비밀번호'}),
        }
		
class Smsform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['phone_number']

		widgets = {
			'phone_number' : forms.TextInput(attrs={'class':'profile_smsInput', 'placeholder':'휴대폰 번호를 입력하세요.'}),

		}

class Smscheckform(forms.ModelForm):
	class Meta:
		model = User
		fields = ['auth_number']
		widgets = {
			'auth_number' : forms.TextInput(attrs={'class':'profile_smsInput', 'placeholder':'인증번호를 입력하세요.'}),

		}