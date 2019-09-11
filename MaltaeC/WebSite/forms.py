from django import forms

class EmailMe(forms.Form):
	name = forms.CharField(required=True)
	email = forms.EmailField()
	subject = forms.CharField(required=True)
	message = forms.CharField(required=True)


class loginForm(forms.Form):
    username_regular = forms.CharField(max_length=300)
    password_regualar = forms.EmailField(required=True)


