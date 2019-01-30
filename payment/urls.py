from django.urls import path
from payment import views
from payment.views import HomePageView, AddToCartView, CartView, CheckOutView, ProcessPaymentView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('product_detail/', AddToCartView.as_view(), name='product_detail'),
    path('show_cart/', CartView.as_view(), name='show_cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('process-payment/', ProcessPaymentView.as_view(), name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]