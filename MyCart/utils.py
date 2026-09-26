def cart_id(request):
    """ Return Current session key or creates a new one. """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart