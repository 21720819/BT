from django import forms
from .models import Review

class UserReviewform(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['rating','content']
 