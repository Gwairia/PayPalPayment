from django.views.generic.base import View
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from E_Payment import settings
from .models import ProductModel, ShippingModel, OrderModel
from .forms import AddToCartForm, ShippingForm
from . import cart
from django.views.decorators.csrf import csrf_exempt


class HomePageView(View):
    def get(self,request):
        count = cart.item_count(request)
        all_products = ProductModel.objects.all()
        context = {'count': count, 'all_products': all_products, }
        return render(request, "payment/index.html", context)
    def post(self,request):
        request.session['product_id']=request.POST.get('id')
        return redirect('product_detail')


class AddToCartView(View):
    def get(self,request):
        count = cart.item_count(request)
        product = get_object_or_404(ProductModel, id=request.session['product_id'])
        form = AddToCartForm()
        context = {'count': count,'product': product, 'form': form }
        return render(request, 'payment/product_detail.html', context)
    def post(self,request):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            request.form_data = form.cleaned_data
            cart.add_item_to_cart(request)
            return redirect('show_cart')


class CartView(View):
    def get(self,request):
        count = cart.item_count(request)
        cart_items = cart.get_all_cart_items(request)
        cart_subtotal = cart.subtotal(request)
        context = {'count': count, 'cart_items': cart_items, 'cart_subtotal': cart_subtotal, }
        return render(request, 'payment/cart.html', context)
    def post(self,request):
        if request.POST.get('submit') == 'Remove':
            cart.remove_item(request)
            return redirect('show_cart')


class CheckOutView(View):
    def get(self,request):
        form = ShippingForm()
        count = cart.item_count(request)
        context = {'form': form,'count':count}
        return render(request, 'payment/checkout.html', context)
    def post(self,request):
        form = ShippingForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            shipping = ShippingModel(name=cleaned_data.get('name'),
                                     email=cleaned_data.get('email'),
                                     postal_code=cleaned_data.get('postal_code'),
                                     address=cleaned_data.get('address'), )
            shipping.save()
            all_items = cart.get_all_cart_items(request)
            for cart_item in all_items:
                order = OrderModel(product_id=cart_item.product_id,
                                   price=cart_item.price,
                                   quantity=cart_item.quantity,
                                   shipping_id=shipping.id)
                order.save()
            cart.clear(request)
            request.session['shipping_id'] = shipping.id
            return redirect('process_payment')


class ProcessPaymentView(View):
    def get(self,request):
        shipping_id = request.session.get('shipping_id')
        shipping = get_object_or_404(ShippingModel, id=shipping_id)
        host = request.get_host()
        paypal_dict = {'business': settings.PAYPAL_RECEIVER_EMAIL,
                       'amount': '%.2f' % shipping.total_cost(),
                       'item_name': 'Order {}'.format(shipping.id),
                       'invoice': str(shipping.id),
                       'currency_code': 'USD',
                       'custom': 'a custom value',
                       'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                       'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
                       'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
                       }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form}
        return render(request, 'payment/process_payment.html', context)


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/payment_done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/payment_cancelled.html')







