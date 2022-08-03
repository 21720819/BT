from django import forms
from .models import Free,Comment

class Freemodelform(forms.ModelForm):
	class Meta:
		model = Free
		fields = ['title','body','photo']

		widgets = {
			'title' : forms.TextInput(
				attrs={'class': 'form-control', 'style': 'width: 400px', 'placeholder': '제목을 입력하세요.', 'name' : 'title', 'id' : 'title'}
			),
			'body' : forms.Textarea (
				attrs={'class': 'form-control', 'cols':'50', 'rows':'15', 'style': 'width: 400px', 'placeholder': '내용을 입력하세요.'}
			),
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']

		widgets = {
			'body' : forms.TextInput(
				attrs={'style': 'width: 746px; height: 40px; padding-left: 10px; border: 1px solid; border-color: lightgrey;border-radius: 7px 7px;', 'placeholder': '댓글을 입력하세요'}
			),
		}