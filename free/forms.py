from django import forms
from .models import Free,Comment

class Freemodelform(forms.ModelForm):
	class Meta:
		model = Free
		fields = ['title','body','photo']

		widgets = {
			'title' : forms.TextInput(
				attrs={ 'class': 'form-control, freeTitle',
           				'style': 'width: 100%; background: rgb(250, 247, 247); border: 0; padding: 0;',
               			'placeholder': '제목을 입력하세요.',
                   		'name' : 'title', 'id' : 'title' }
			),
			'body' : forms.Textarea (
				attrs={ 'class': 'form-control, freeBody',
           				'cols':'50', 'rows':'10',
               			'style': 'width: 100%; height: 180px; resize: none; background: rgb(250, 247, 247); border: 0; padding: 0;',
                  		'placeholder': '내용을 입력하세요.' }
			),
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']

		widgets = {
			'body' : forms.TextInput(
				attrs={'class': 'comment', 'placeholder': '댓글을 입력하세요.'}
			),
		}