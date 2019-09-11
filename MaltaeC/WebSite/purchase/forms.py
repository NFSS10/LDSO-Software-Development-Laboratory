

from django import forms

from .models import Product
from datetime import date, datetime
from calendar import monthrange



class PurchaseForm(forms.Form):
    product = forms.CharField(max_length=300)
    user = forms.CharField(max_length=300)
    quantidade = forms.IntegerField()

class CreditCardField(forms.IntegerField):
    def clean(self, value):
        """Check if given CC number is valid and one of the
           card types we accept"""
        if value:
            if len(value) < 13 or len(value) > 16:
                raise forms.ValidationError("Please enter in a valid " + \
                                            "credit card number.")
        return super(CreditCardField, self).clean(value)


class CCExpWidget(forms.MultiWidget):
    """ Widget containing two select boxes for selecting the month and year"""

    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]

    def format_output(self, rendered_widgets):
        html = u' / '.join(rendered_widgets)
        return u'<span style="white-space: nowrap;">%s</span>' % html




class BillingForm(forms.Form):
    number = CreditCardField(required=True, label="Card Number")
    expiration = forms.DateField(initial=datetime.today)
    cvc = forms.IntegerField(required=True, label="CCV Number",max_value=9999, widget=forms.TextInput(attrs={'size': '4'}))