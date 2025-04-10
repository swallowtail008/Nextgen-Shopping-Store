from django.shortcuts import render,redirect
from .models import * 
from django.db.models import Q
from .models import Product
from django.contrib import messages
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import WishlistItem
from django.shortcuts import render, get_object_or_404


def home(request):
    user = request.user
    total = 0
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user)
        len_user = len(cart)
        print(len_user)
        if cart:
            total = 0
            total_amount = 0
            for i in cart:
                total_amount = (i.quantity) * (i.product.current_price)
                total = total + total_amount

    slides = Slider.objects.all()
    Products = Product.objects.all()
    feture_pro = Products.filter(featured_product=True)
    trending_pro = Products.filter(trending_product=True)
    top_seller = Products.filter(top_seller=True)
    deals_of_the_day = Products.filter(deals_of_the_day=True)

    return render(request, 'home.html',
                  # {'slides': slides, 'feture_pro': feture_pro, 'trending_pro': trending_pro, 'top_seller': top_seller,
                  #  'deals_of_the_day': deals_of_the_day, 'len_user': len_user ,'carts':cart ,'total':total},
                  locals()
                  )

def super_sub_prod(request,id):
        super_sub_Category = Super_SubCategory.objects.get(id=id)
        prod = Product.objects.filter(super_sub_Category=super_sub_Category)
        return render(request, 'product/super_sub_prod.html', locals())

def add_to_cart(request, id):
    user = request.user
    prod = Product.objects.get(id=id)


    if user.is_authenticated:
        try:
            cart = Cart.objects.get(Q(user=user, product=prod))
            cart.quantity+= 1
            cart.save()
            return redirect('home')
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user, product=prod)
            cart.save()
            return redirect('home')
def remove_cart(request,id):
    user = request.user
    cart = Cart.objects.get(Q(user=user, id=id))
    cart.delete()
    return redirect('cart_page')

def cart_page(request):
    user = request.user
    total = 0
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user)
        len_user = len(cart)
        if cart:
            total = 0
            total_amount = 0
            for i in cart:
                total_amount = (i.quantity) * (i.product.current_price)
                total = total + total_amount
                
                ship_total=total + 75

    return render(request,'product/cart_page.html',locals())

def increase(request,id):
    user = request.user
    cart = Cart.objects.get(Q(user=user, product=id))
    cart.quantity += 1
    if cart.quantity>cart.product.quantity:
        cart.quantity += 0
        messages.warning(request,"Product quantity not available")
        return redirect('cart_page')
    cart.save()
    return redirect('cart_page')

def decries(request,id):
    user = request.user
    cart = Cart.objects.get(Q(user=user, product=id))
    cart.quantity -= 1
    if cart.quantity == 0:
        cart.delete()
        return redirect('cart_page')
    cart.save()
    return redirect('cart_page')

@csrf_exempt
def sslcommerz_Success(request):
    # user = request.user
    # # if user.is_authenticated:
    # cart = Cart.objects.filter(user=user)
    # if not cart:
    #         return redirect('fail')

    # total_ammount = sum(item.total_price() for item in cart)

    # order = Oder.objects.create(

    #         user = user,
    #         total_ammount = total_ammount,
    #         payment_status = 'paid',
    #     )
    # for item in cart:
    #     order.products.add(item.product)

    # cart.delete()
    return render(request, 'product/success.html')


@csrf_exempt
def sslcommerz_Fail(request):

    # user = request.user
    # # if user.is_authenticated:
    # cart = Cart.objects.filter(user=user)
    # if not cart:
    #         return redirect('fail')

    # total_ammount = sum(item.total_price() for item in cart)

    # order = Oder.objects.create(

    #         user = user,
    #         total_ammount = total_ammount,
    #         payment_status = 'Unpaid',
    #     )
    # for item in cart:
    #     order.products.add(item.product)

    return render(request, 'product/fail.html')

def sslcommerz_payment(request):
    user = request.user
    cart = [p for p in Cart.objects.all() if p.user == user]

    if cart:
        total = 0
        shipping_cost=75
        for i in cart:
            total_amount = (i.quantity) * (i.product.current_price)
            total = total + total_amount
            ship_total = total + shipping_cost
 
    sslcz = SSLCOMMERZ(
        {'store_id': 'ecomm672dde1f2e101', 'store_pass': 'ecomm672dde1f2e101@ssl', 'issandbox': True})
    total_amounts = request.GET.get('totalAmu')

    data = {

        # set_urls -----------------------------------------------------------------
        'success_url': "http://127.0.0.1:8000/Success_Order/success/",
        'fail_url': "http://127.0.0.1:8000/fail_order/Fail/",
        # 'cancel_url': "http://127.0.0.1:8000/fail_order/",
        # ---------------------------------------------------------------------------

        # set_product_integration---------------------------------------------------
        'total_amount': ship_total,
        'currency': "BDT",
        'product_category': "Computers Accessories",
        'product_name': "Computers Accessories",
        'num_of_item': 1,
        'shipping_method': "NO",
        'product_profile': "general",
        # ---------------------------------------------------------------------------

        # set_customer_info --------------------------------------------------------
        # user = request.user
        'cus_name': user.username,
        'cus_email': user.email,
        # ---------------------------------------------------------------------------

        # set_shipping_info --------------------------------------------------------
        'cus_add1': "customer address",
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'cus_phone': "01515612682",
        # --------------------------------------------------------------------------

        'tran_id': "tran_12345",
        'emi_option': "0",
        'multi_card_name': "",

    }

    response = sslcz.createSession(data)
    return redirect(response['GatewayPageURL'])
    # API response
    print(response)
    # Need to redirect user to response['GatewayPageURL']

def Search(request):
    query = request.GET.get('query')
    product = Product.objects.filter(title__icontains = query)
    context = {
        'product':product
    }
    return render(request, 'product/search.html',context)


def wishlist(request):
    Products = Product.objects.all()
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'product/wishlist.html', locals())
    

@login_required
def remove_from_wishlist(request,id):
    user = request.user
    wishlist = WishlistItem.objects.get(Q(user=user, id=id))
    wishlist.delete()
    return redirect('wishlist')



from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, id):
    Products = Product.objects.filter(id=id)


    return render(request, 'product/product_detail.html', locals())