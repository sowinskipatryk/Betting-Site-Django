from django.contrib.auth.forms import UserCreationForm
from .models import User, Coupon
from django import forms


class RegisterForm(UserCreationForm):
	vmail = forms.EmailField(label="Email address confirmation")

	class Meta:
		model = User
		fields = ['username', 'email', 'vmail', 'password1', 'password2']

	# def clean(self):
	# 	clean_data = super().clean()
	# 	email = clean_data['email']
	# 	vmail = clean_data['verify_email']
	#
	# 	if email != vmail:
	# 		raise forms.ValidationError("Emails don't match")
