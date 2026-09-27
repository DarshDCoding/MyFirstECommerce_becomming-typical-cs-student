from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import CartItem, Cart

from MyCart.utils import cart_id as _cart_id


# Create your views here.
def _get_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(cart = cart, product = product)

    return cart_item

def add_item(request, product_id):
    product = Product.objects.get(id=product_id)

    # try:
    #     cart = Cart.objects.get(cart_id = _cart_id(request))
    # except Cart.DoesNotExist:
    #     cart = Cart.objects.create(cart_id = _cart_id(request))
    # cart.save()
    cart, _ = Cart.objects.get_or_create(cart_id= _cart_id(request))



    # try:
    #     cart_item = CartItem.objects.get(cart = cart, product = product)
    #     cart_item.quantity += 1
    # except CartItem.DoesNotExist:
    #     cart_item = CartItem.objects.create(cart = cart, product = product, quantity = 1)
    # cart_item.save()
    cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def remove_item(request, product_id):
    cart_item = _get_cart_item(request, product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def delete_item(request, product_id):
    cart_item = _get_cart_item(request, product_id)
    cart_item.delete()
    return redirect('cart')


def cart(request):
    total = 0
    quantity = 0
    taxed_total = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)

        for items in cart_items:
            total += items.quantity * items.product.price
            taxed_total += (items.quantity * items.product.get_taxed_price())
            quantity += items.quantity

        grand_total = total + taxed_total

    except ObjectDoesNotExist:
        cart_items = None

    context = {
        'total': total,
        'cart_items': cart_items,
        'quantity': quantity,
        'tax': taxed_total,
        'grand_total': grand_total,
    }

    return render(request, 'cart/cart.html', context)
