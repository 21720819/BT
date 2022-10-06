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
 