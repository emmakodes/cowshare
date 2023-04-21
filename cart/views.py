from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from cowshare.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm
from django.db.models import Sum
from orders.models import Order, OrderItem
from django.contrib import messages

@require_POST
def cart_add(request, product_id):
    emessage = ""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    total = OrderItem.objects.filter(product=product,order__paid=True,order__verified=True).aggregate(Sum('quantity'))['quantity__sum']
    if not total:
        total = 0
    remaining_shares = (product.sharing_number - total)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['quantity'] <= remaining_shares:
            cart.add(product=product,
                    quantity=cd['quantity'],
                    override_quantity=cd['override'])
        else:
            emessage = "Quantity is more than remaining shares"
            return render(request, 'cart/detail.html', {'emessage': emessage})
            # messages.error(request,"Quantity is more than remaining shares")

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    categories = Category.objects.all()
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'cart/detail.html', {'cart': cart,'categories':categories})




# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     total = OrderItem.objects.filter(product=product,order__paid=True,order__verified=True).aggregate(Sum('quantity'))['quantity__sum']
#     remaining_shares = product.sharing_number - total
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         if cd['quantity'] <= remaining_shares:
#             cart.add(product=product,
#                     quantity=cd['quantity'],
#                     override_quantity=cd['override'])
#         else:
#             messages.error(request,"Quantity is more than remaining shares")
#     return redirect('cart:cart_detail')