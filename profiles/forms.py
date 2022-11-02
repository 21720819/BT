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

class PostReportform(forms.ModelForm):
	class Meta:
		model = ReportPost
		fields = ['content','category']
