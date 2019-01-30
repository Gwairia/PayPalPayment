from .models import CartModel, ProductModel
from django.shortcuts import get_object_or_404


def cart_id(request):
    if 'cart_id' not in request.session:
        request.session['cart_id'] = generate_cart_id()
    return request.session['cart_id']


def generate_cart_id():
    import string, random
    return ''.join([random.choice(string.ascii_letters + string.digits) in range(50)])


def get_all_cart_items(request):
    return CartModel.objects.filter(cartID = cart_id(request))


def add_item_to_cart(request):
    product_id = request.session['product_id']
    quantity = request.form_data['quantity']

    prod = get_object_or_404(ProductModel, id=product_id)
    price = prod.price
    cart_items = get_all_cart_items(request)
    item_in_cart = False

    for cart_item in cart_items:
        if cart_item.product_id == product_id:
            cart_item.update_quantity(quantity)
            item_in_cart = True

    if not item_in_cart:
        item = CartModel(
            cartID = cart_id(request),
            price = price,
            quantity = quantity,
            product_id = product_id,
        )
        item.save()


def item_count(request):
    return get_all_cart_items(request).count()


def subtotal(request):
    cart_item = get_all_cart_items(request)
    sub_total = 0
    for item in cart_item:
        sub_total += item.total_cost()
    return sub_total


def remove_item(request):
    item_id = request.POST.get('item_id')
    citem = get_object_or_404(CartModel, id=item_id)
    citem.delete()


def clear(request):
    cart_items = get_all_cart_items(request)
    cart_items.delete()
