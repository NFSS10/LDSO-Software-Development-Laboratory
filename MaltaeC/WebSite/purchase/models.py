from django.db import models
from django.conf import settings
from WebSite.utilizadores.models import BaseUser
from WebSite.products.models import Product


class Purchase(models.Model):
    user = models.ForeignKey('utilizadores.BaseUser', on_delete=models.CASCADE)
    estado = models.CharField(max_length=300)
    charge_id = models.CharField(max_length=32, blank=True)
    total_price = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    card_number = models.BigIntegerField(default=1)
    card_exp_month = models.IntegerField(default=1)
    card_exp_year = models.IntegerField(default=1)
    cvc = models.IntegerField(default=1)

    def __init__(self, *args, **kwargs):
        super(Purchase, self).__init__(*args, **kwargs)

        # bring in stripe, and get the api key from settings.py
        import stripe
        stripe.api_key = settings.STRIPE_API_KEY

        self.stripe = stripe

    def charge(self, price, number, exp_month, exp_year, cvc):
        """
        Takes a the price and credit card details: number, exp_month,
        exp_year, cvc.

        Returns a tuple: (Boolean, Class) where the boolean is if
        the charge was successful, and the class is response (or error)
        instance.
        """

        if self.charge_id:  # don't let this be charged twice!
            return False, Exception(message="Already charged.")

        try:
            response = self.stripe.Charge.create(
                amount=price,
                currency="eur",
                card={
                    "number": number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,

                    #### it is recommended to include the address!
                    # "address_line1" : self.address1,
                    # "address_line2" : self.address2,
                    # "daddress_zip" : self.zip_code,
                    # "address_state" : self.state,
                },
                description='Thank you for your purchase!')

            self.charge_id = response.id

        except self.stripe.CardError as ce:
            # charge failed
            return False, ce

        return True, response


class PurchaseItem(models.Model):
    purchase = models.ForeignKey('Purchase', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantidade = models.CharField(max_length=300)
