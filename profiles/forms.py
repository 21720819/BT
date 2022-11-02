from tkinter import Widget
from django import forms
from .models import Review, ReportUser,ReportPost

class UserReviewform(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['rating','content']

class UserReportform(forms.ModelForm):
	class Meta:
		model = ReportUser
		fields = ['content','category']

		widgets = {
			'category' : forms.Select(
				attrs={ 'class': 'custom-select', 'style': 'width: 100%; height: 20px; background: #fff; border: 0; margin-bottom: 15px;' }
			),
		}
  
class PostReportform(forms.ModelForm):
	class Meta:
		model = ReportPost
		fields = ['content','category']

		widgets = {
			'category' : forms.Select(
				attrs={ 'class': 'custom-select', 'style': 'width: 100%; height: 20px; background: #fff; border: 0; margin-bottom: 15px;' }
			),
		}