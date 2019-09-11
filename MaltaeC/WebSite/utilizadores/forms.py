from django import forms

class ResetPasswordConfirmForm(forms.Form):
	new_password = forms.CharField(max_length=16, widget=forms.PasswordInput)
	new_password_confirm = forms.CharField(max_length=16, widget=forms.PasswordInput)

class ResetPasswordForm(forms.Form):
	email = forms.EmailField(required=True)
	
class RegisterForm(forms.Form):
    username_regular = forms.CharField(max_length=300)
    email_regular = forms.EmailField(required=True)
    password_regular = forms.CharField(max_length=16, widget=forms.PasswordInput)
    password_confirm_regular = forms.CharField(max_length=16, widget=forms.PasswordInput)
    phone_regular = forms.CharField(max_length=16)
    address_regular = forms.CharField(max_length=500)

class RegisterArtesaoForm(forms.Form):
	username = forms.CharField(max_length=300)
	email = forms.EmailField(required=True)
	password = forms.CharField(max_length=16, widget=forms.PasswordInput, required=True)
	password_confirm_maker = forms.CharField(max_length=16, widget=forms.PasswordInput, required=True)
	phone_maker = forms.CharField(max_length=16)
	# Google API maps
	geolocation = forms.CharField()
	latitude = forms.FloatField()
	longitude = forms.FloatField()
	areatexto = forms.CharField(max_length=1000, required=True)
	

class EditUserProfileForm(forms.Form):
	name = forms.CharField(max_length=300,required=False)
	new_password = forms.CharField(max_length=16, widget=forms.PasswordInput,required=False)
	old_password = forms.CharField(max_length=16, widget=forms.PasswordInput,required=False)
	phone_number = forms.CharField(max_length=16,required=False)
	adress = forms.CharField(max_length=300,required=False)
	bio = forms.CharField(required=False)
	
class EditArtistProfileForm(forms.Form):
	name = forms.CharField(max_length=300,required=False)
	new_password = forms.CharField(max_length=16, widget=forms.PasswordInput,required=False)
	old_password = forms.CharField(max_length=16, widget=forms.PasswordInput,required=False)
	phone_number = forms.CharField(max_length=16,required=False)
	geolocation = forms.CharField(required=False)
	latitude = forms.FloatField(required=False)
	longitude = forms.FloatField(required=False)
	bio = forms.CharField(required=False)
	
class LoginForm(forms.Form):
	username = forms.CharField(max_length=300)
	password = forms.CharField(max_length=16, widget=forms.PasswordInput)