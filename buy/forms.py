from django import forms
from .models import Buy

class BuyModelform(forms.ModelForm):
	class Meta:
		model = Buy
		fields = ['title','body','date','category','wpeople','price','location','photo']

		widgets = {
			'photo' : forms.ClearableFileInput(
				attrs={ 'style': 'visibility: hidden; position: absolute; z-index: 1;',
           				'onchange': 'imageView(this)',
						'name' : 'photo', 'id' : 'photo' }
			),
			'category' : forms.Select(
				attrs={ 'class': 'custom-select', 'style': 'border: 0;' }
			),
			'title' : forms.TextInput(
				attrs={ 'class': 'form-control, detail_title', 
						'style': 'border: 0; padding: 0;',
						'placeholder': '제목을 입력하세요.',
						'name' : 'title', 'id' : 'title' }
			),
			'price' : forms.TextInput(
				attrs={ 'class': 'form-control, detail_price',
						'style': 'width: 70px; border: 0; text-align: right; padding: 0; display: inline-block;',
						'name' : 'price', 'id' : 'price' }
			),
			'wpeople' : forms.TextInput(
				attrs={ 'class': 'form-control, detail_price',
						'style': 'width: 35px; border: 0; text-align: right; padding: 0; display: inline-block;',
						'name' : 'wpeople', 'id' : 'wpeople '}
			),
			'location' : forms.TextInput(
				attrs={ 'class': 'form-control', 'class': 'detail_loca_time',
						'style': 'width: 100%; border: 0; outline: none; padding: 0;',
						'placeholder': '장소를 입력하세요. ',
						'name' : 'place', 'id' : 'place' }
			),
			# 'lat' : forms.TextInput(
			# 	attrs={'class' : 'form-control', 'type' : 'hidden',}
			# 	),
            # 'long' : forms.TextInput(
			# 	attrs={'class' : 'form-control', 'type' : 'hidden',}
			# 	),
			'date' : forms.TextInput(
				attrs={ 'class': 'form-control', 'class': 'detail_loca_time',
						'style': 'width: 100%; border: 0; padding: 0;',
						'placeholder': '날짜를 입력하세요.',
						'name' : 'date', 'id' : 'date' }
			),
			'body' : forms.Textarea (
				attrs={ 'class': 'form-control, detail_context', 'cols':'50', 'rows':'10',
						'style': 'width: 100%; border: 0; margin: 0 0 40px 0; padding: 0;',
						'placeholder': '내용을 입력하세요.' }
			),
		}