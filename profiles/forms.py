from tkinter import Widget
from django import forms
from .models import Review, ReportUser

class UserReviewform(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['rating','content']

class UserReportform(forms.ModelForm):
	class Meta:
		model = ReportUser
		fields = ['content']
  
		# label = ""
  
		# widgets = {
		#  	'content' : forms.Textarea(
		#  		attrs={ 'class': 'form-control, detail_context', 'cols':'50', 'rows':'10',
		#  				'style': 'width: 100%; resize: none; border: 0; margin: 0; padding: 0; ',
		#  				'placeholder': '내용을 입력하세요.'
      	# 				}
		# 	)
		# }