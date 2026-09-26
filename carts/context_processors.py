from .models import CartItem, Cart
from django.db.models import Sum
from MyCart.utils import cart_id

#TODO: create cart items count by getting current cart session id and quantity of cart_items

def cart_item_count(request):

    try:
        cart= Cart.objects.get(cart_id=cart_id(request))
        if cart:
            cart_items_count = CartItem.objects.filter(
                cart=cart,
                is_active=True
            ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    except Cart.DoesNotExist:
        cart_items_count = 0

    return {'cart_items_count': cart_items_count}
