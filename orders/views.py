from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderCreateForm
# from .tasks import order_created
from cart.cart import Cart
from django.conf import settings
from cowshare.models import Category, Product
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.db.models import Sum
from cowshare.models import Message
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    categories = Category.objects.all()
    cart = Cart(request)
    if request.method == 'POST':
        pk = settings.PAYSTACK_PUBLIC_KEY
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            print('amount value suppose x100',order.amount_value)
            return render(request,
                          'orders/order/make_payment.html',
                          {'payment': order,'field_values': request.POST,'paystack_pub_key': pk,'amount_value': order.amount_value(),'amount':order.get_total_cost()})            
            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form, 'categories':categories})
    
    
# def initiate_payment(request):
#     if request.method == "POST":
#         amount = request.POST['amount']
#         email = request.POST['email']

#         pk = settings.PAYSTACK_PUBLIC_KEY

#         payment = OrderItem.objects.create(amount=amount, email=email, user=request.user)
#         payment.save()

#         context = {
#             'payment': payment,
#             'field_values': request.POST,
#             'paystack_pub_key': pk,
#             'amount_value': payment.amount_value(),
#         }
#         return render(request, 'make_payment.html', context)

#     return render(request, 'payment.html')

@login_required
def verify_payment(request, ref):
    payment = Order.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        payment.paid = True
        # user_wallet = Order.objects.get(user=request.user)
        # user_wallet.balance += payment.amount
        payment.save()
        
        #products = Product.objects.filter(items__order__ref=ref)
        # order_items = OrderItem.objects.filter(order__ref=ref)
        # print('order item: ',order_items)
        # product = order_items.product
        # print(product)
        # total_ordered = OrderItem.objects.filter(product=product).aggregate(total_ordered=models.Sum('quantity'))['total_ordered'] or 0
        # print('total order: ',total_ordered)
        
        
        
        
        # assume we have an order with id=1
        #order = Order.objects.get(id=1)

        # get all order items for the order
        order_items = payment.items.all()
        # order_items = order_items.objects.filter(items__paid=True,items__verified=True)
        # get all products for the order
        products = []
        for order_item in order_items:
            product = order_item.product
            products.append(product)      
        
        print('all products',products)
        
        for product in products:
            
        
        
        
        
        
            total_ordered = OrderItem.objects.filter(product=product,order__paid=True,order__verified=True).aggregate(total_ordered=models.Sum('quantity'))['total_ordered'] or 0
            print('total order: ',total_ordered)        
            if total_ordered == product.sharing_number:
                # Send email to all users who made orders for this product
                product.available = False
                product.save()
                new_product = Product()
                new_product.category = product.category
                new_product.image = product.image
                new_product.description = product.description
                new_product.subcategory = product.subcategory
                new_product.name = product.name
                new_product.price = product.price
                new_product.sharing_price = product.sharing_price
                new_product.available = True
                new_product.sharing_number = product.sharing_number
                new_product.gender = product.gender
                new_product.save()
                
                message = Message.objects.create(user=request.user, user_message='Your order for Product ID: {} is due for delivery and  will be sent in two days.'.format(product.id))
                orders = Order.objects.filter(items__product=product).distinct()
                recipients = [order.user.email for order in orders]
                print(orders)
                print('recipients', recipients)

                message = "Your order on meatyshares.com for Product ID: {} is due for delivery and  will be sent in two days. Thank you for patronizing meatyshares.com".format(product.id)
                send_mail('Order ready for shipping', message, settings.EMAIL_HOST_USER, recipients, fail_silently=False)        
            

        
        
        
        
        
        # ref_orders = Order.objects.filter(ref=ref)
        # product_ids = ref_orders.values_list('order_items__product__id', flat=True)
        # products = Product.objects.filter(id__in=product_ids)



        
        
        print(request.user.username, "order was successful")
        return render(request, "orders/order/success.html", {'exref':ref})
    return render(request, "orders/order/success.html", {'exref':ref})




@login_required
def exclusions(request, exref):
    ex_message = ""
    exorders = Order.objects.get(ref=exref)
    if request.method == 'POST':
        exclusion = request.POST.get('exclusion', None)
        exorders.parts_to_exclude = exclusion
        exorders.save()
        ex_message = "Your exclusion is recorded successfully!"
    return render(request, "orders/order/success2.html", {'ex_message':ex_message})




# from django.core.mail import send_mail

# product = Product.objects.get(id=product_id)
# total_ordered = OrderItem.objects.filter(product=product).aggregate(total_ordered=models.Sum('quantity'))['total_ordered'] or 0

# if total_ordered == product.sharing_number:
#     # Send email to all users who made orders for this product
#     orders = Order.objects.filter(items__product=product).distinct()
#     recipients = [order.user.email for order in orders]

#     message = "Your order for {} will be sent in two days.".format(product.name)
#     send_mail('Order ready for shipping', message, 'noreply@example.com', recipients, fail_silently=False)
