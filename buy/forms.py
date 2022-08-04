from django import forms
from .models import Buy

class BuyModelform(forms.ModelForm):
	class Meta:
		model = Buy
		fields = ['title','body','date','category','wpeople','price','location','photo']

		widgets = {
			'title' : forms.TextInput(
				attrs={'class': 'form-control', 'style': 'width: 400px', 'placeholder': '제목을 입력하세요.', 'name' : 'title', 'id' : 'title'}
			),
			'body' : forms.Textarea (
				attrs={'class': 'form-control', 'cols':'50', 'rows':'15', 'style': 'width: 400px', 'placeholder': '내용을 입력하세요.'}
			),
			'date' : forms.TextInput(
				attrs={'class': 'form-control', 'style': 'width: 200px', 'placeholder': '날짜를 입력하세요.', 'name' : 'date', 'id' : 'date'}
			),
			'price' : forms.TextInput(
				attrs={'class': 'form-control', 'style': 'width: 150px', 'name' : 'price', 'id' : 'price'}
			),
			'wpeople' : forms.TextInput(
				attrs={'class': 'form-control', 'style': 'width: 100px', 'name' : 'wpeople', 'id' : 'wpeople'}
			),
			'location' : forms.TextInput(
				attrs={'class': 'form-control', 'style': 'width: 200px', 'placeholder': '장소를 입력하세요. ', 'name' : 'place', 'id' : 'place'}
			),
			'category' : forms.Select(
				attrs={'class': 'custom-select'}
			),
		}