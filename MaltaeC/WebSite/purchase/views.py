#!/usr/bin/env python
# -*- coding: utf-8 -*-

import stripe
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PurchaseForm
from django.db import transaction
from django.conf import settings
from WebSite.utilizadores.models import BaseUser
from WebSite.cart.models import Cart, CartItem
from .models import Purchase, PurchaseItem
from .forms import BillingForm
from django.core.mail import send_mail

# Create your views here.
#

stripe.api_key = settings.STRIPE_API_KEY


@transaction.atomic
def paymentTransaction(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BillingForm(request.POST)
            if form.is_valid():

                cart = Cart.objects.get(user_id=request.user.id)
                items = CartItem.objects.filter(cart=cart)
                sum = 0
                for item1 in items:
                    sum += item1.product.original_price

                purchase = Purchase(user=request.user, estado='EM ESPERA', total_price=sum,
                                    card_number=form.cleaned_data['number'],
                                    card_exp_month=form.cleaned_data['expiration'].month,
                                    card_exp_year=form.cleaned_data['expiration'].year,
                                    cvc=form.cleaned_data['cvc']
                                    )
                purchase.save()

                for item in items:
                    p = PurchaseItem(purchase=purchase, product=item.product, quantidade=item.quantidade)
                    p.save()
                CartItem.objects.filter(cart=cart).delete()
                return show_user_purchases(request)


def process(request, purchaseid):
    if request.user.is_authenticated and request.user.is_staff:

        purchase = Purchase.objects.get(pk=purchaseid)
        purchase.charge(int(purchase.total_price * 100), purchase.card_number, purchase.card_exp_month,
                        purchase.card_exp_year,
                        purchase.cvc)
        Purchase.objects.filter(pk=purchaseid).update(estado='PROCESSADO')
        purchases = Purchase.objects.all()
        send_mail('MaltaC Compra',
              'O seu pedido de compra foi aceite e foi procedido ao envio',
              settings.DEFAULT_FROM_EMAIL,
              [purchase.user.email],
              )
    return render(request, 'AdminPurchasesAllTime.html', {'purchases': purchases})


def cancel(request, purchaseid):
    if request.user.is_authenticated and request.user.is_staff:

        Purchase.objects.filter(pk=purchaseid).update(estado='NAO AUTORIZADA')
        purchase = Purchase.objects.get(pk=purchaseid)
        purchases = Purchase.objects.all()
        send_mail('MaltaC Compra',
              'O seu pedido de compra foi rejeitado para mais informações contacte',
              settings.DEFAULT_FROM_EMAIL,
              [purchase.user.email],
              )
    return render(request, 'AdminPurchasesAllTime.html', {'purchases': purchases})


def show_user_purchases(request):
    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user.id)
        return render(request, 'UserPurchases.html', {'purchases': purchases})


def show_purchases_pending(request):
    if request.user.is_authenticated and request.user.is_staff:
        purchases = Purchase.objects.filter(estado='EM ESPERA')
        return render(request, 'AdminSeePendingPurchases.html', {'purchases': purchases})


def show_purchase(request, purchaseid):
    if request.user.is_authenticated:
        purchase = Purchase.objects.get(pk=purchaseid)
        purchaseItems = PurchaseItem.objects.filter(purchase=purchase)
        sumatorio = 0
        for item in purchaseItems:
            sumatorio += item.product.original_price
        return render(request, 'Purchase.html', {'purchaseItems': purchaseItems, 'sumatorio': sumatorio})


def checkout(request):
    return render(request, 'Billing.html')


def show_All_purchases(request):
    purchases = Purchase.objects.all()
    return render(request, 'AdminPurchasesAllTime.html', {'purchases': purchases})
