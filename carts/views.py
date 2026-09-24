from django.shortcuts import render, redirect

from store.models import Product
from .models import CartItem, Cart


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart

def add_item(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(cart = cart, product = product)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart = cart, product = product, quantity = 1)
    cart_item.save()

    return redirect('cart')

def cart(request):
    products = CartItem.objects.all()
    total_price = 0
    data= []
    for product in products:
        total_price += product.product.price*product.quantity
        data.append({
            'product_name': product.product.product_name,
            'image': product.product.images.url,
            'quantity': product.quantity,
            'price': product.product.price,
            'total_price': product.product.price * product.quantity
        })
    context = {'products': data, 'total_price': total_price}

    return render(request, 'cart/cart.html', context)