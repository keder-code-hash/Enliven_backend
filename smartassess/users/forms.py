from django.forms import ModelForm
from django.core.validators import validate_email
from django import forms
from django.forms import ModelForm
from .models import Register

class RegisterForm(forms.Form):
	first_name=forms.CharField(max_length=40)
	last_name=forms.CharField(max_length=20)
	user_name=forms.CharField(max_length=20)
	emailid=forms.CharField(max_length=100)
	user_password=forms.CharField(max_length=20,required=True)
	user_password_conf=forms.CharField(max_length=20,required=True)

	
	def clean_emailid(self):
		cleaned_data=super().clean()
		emailid=cleaned_data.get('emailid')
		if validate_email(emailid):
			msg='Invalid emailid'
			self.add_error('emailid',msg)
		return emailid
	def clean(self):
		cleaned_data =super().clean()
		passw=cleaned_data.get('user_password')
		conf_password=cleaned_data.get('user_password_conf')
		if conf_password!=passw:
			msg2='password does not match'
			msg1='enter the password again'
			self.add_error('user_password_conf',msg2)
			self.add_error('user_password',msg1)
		return cleaned_data

class LogInForm(forms.Form):
	emailid = forms.CharField(max_length=50,required=True)
	user_password = forms.CharField(max_length=50, required=True)

	def clean_emailid(self):
		cleaned_data=super().clean()
		emailid=cleaned_data.get('emailid')
		if validate_email(emailid):
			msg='Invalid emailid'
			self.add_error('emailid',msg)
		else:
			pass
		return emailid

	def clean(self):
		cleaned_data=super(LogInForm, self).clean()
		email_id=cleaned_data.get('emailid')
		if Register.objects.filter(email__exact=email_id).exists()==False:
			msg="User does not exist.Check The Email"
			self.add_error('emailid',msg)
		else:
			user=Register.objects.get(email__exact=email_id)
			if user.check_password(cleaned_data.get('user_password'))==False:
				msg="password does not match"
				self.add_error('user_password',msg)
			else:
				pass
		return cleaned_data
class profileForm(forms.Form):
	user_name = forms.CharField(max_length=20,required=False)
	first_name = forms.CharField(max_length=40,required=False)
	last_name = forms.CharField(max_length=20,required=False)
	date_of_birth = forms.DateField(required=False)
	bio = forms.CharField(max_length=100,required=False)
	interests = forms.CharField(max_length=200,required=False)
	ph_no=forms.CharField(max_length=10,required=False)
	def clean(self):
		cleaned_data=super().clean()
		return cleaned_data

class resetPassInit(forms.Form):
	email=forms.EmailField(max_length=200,required=True)
	def clean(self):
		cleaned_data =super().clean()
		email=cleaned_data.get('email')
		user=Register.objects.filter(email=email)
		if user.exists() is False:
			msg='user with this email does not exist.Provide the verified email.'
			self.add_error('email',msg)
		return cleaned_data