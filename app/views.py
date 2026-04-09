from django.shortcuts import render, redirect
from .models import *

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                'name': request.user.username,
                'email': request.user.email,
            }
        )
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0
        }

    context = {'items': items, 'order': order}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                'name': request.user.username,
                'email': request.user.email,
            }
        )
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0
        }

    context = {'items': items, 'order': order}
    return render(request, 'app/checkout.html', context)