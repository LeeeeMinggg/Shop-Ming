from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def search(request):
    return render(request,'app/search.html')
def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request,'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Tên đăng nhập hoặc mật khẩu sai!')

    return render(request, 'app/login.html')
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
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
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0
        }
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
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
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0
        }
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
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
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0
        }
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order,  'cartItems': cartItems}
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    try:
        data = json.loads(request.body)
        productId = data.get('productId')
        action = data.get('action')

        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                'name': request.user.username,
                'email': request.user.email,
            }
        )

        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItems = OrderItem.objects.filter(order=order, product=product)

        if orderItems.exists():
            orderItem = orderItems.first()
        else:
            orderItem = OrderItem.objects.create(order=order, product=product, quantity=0)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        if orderItem.quantity <= 0:
            orderItem.delete()
        else:
            orderItem.save()

        return JsonResponse({'message': 'updated successfully'})

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        print('updateItem error:', e)
        return JsonResponse({'error': str(e)}, status=500)