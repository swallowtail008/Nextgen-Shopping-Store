from django.urls import path
from .views import *
urlpatterns = [
    path('', home,name='home'),
    path('super_sub_prod/<int:id>/', super_sub_prod,name='super_sub_prod'),
    path('add_to_cart/<int:id>/', add_to_cart,name='add_to_cart'),
    path('remove_cart/<int:id>/', remove_cart,name='remove_cart'),
    path('cart_page/', cart_page,name='cart_page'),
    path('decries/<int:id>/',decries,name='decries'),
    path('increase/<int:id>/',increase,name='increase'),
    path('Success_Order/success/', sslcommerz_Success, name='Success_Order'),
    path('fail_order/Fail/', sslcommerz_Fail, name='fail_order'),
    path('payment/', sslcommerz_payment, name='payment'),
    path('search/', Search, name='search'),
    path('wishlist/',wishlist, name='wishlist'),
    path('wishlist/<int:id>/', remove_from_wishlist,name='remove_from_wishlist'),
    path('product/<int:id>/',product_detail, name='product_detail'),
]
