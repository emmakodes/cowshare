from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem, ExchangeOffer, ExchangeOfferResponse
from .models import UserProfile, Product, Category, SubCategory, Message, CustomUser
from django.db.models import F
from django.db.models import Sum
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from allauth.account.models import EmailConfirmationHMAC
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Subquery, OuterRef


# Create your views here.
def index(request):
    categories = Category.objects.all()
    # get all products ordered by category name
    try:
        products = Product.objects.select_related('category').order_by('category__name')
        # iterate over the products
        first_product = products[0]
        products = products[1:]
    except: 
        no_product_message = "No product available yet!"
        context = {
            'no_product_message': no_product_message,
        }
        return render(request, 'cowshare/index.html',context)
        
    
    context = {
        'categories': categories,
        'first_product': first_product,
        'products': products,
    }
    return render(request, 'cowshare/index.html',context)

@login_required
def profile(request):
    categories = Category.objects.all()
    orders = Order.objects.filter(user=request.user)
    print(orders)
    order_itemz = OrderItem.objects.filter(order__user=request.user)
    print(order_itemz)

    
    
    
    order_items = OrderItem.objects.filter(order__in=orders).select_related('product')
    userproducts = Product.objects.filter(id__in=[item.product.id for item in order_items]).annotate(names=F('name'),imagef=F('image'))
    print(userproducts)
    print(order_items)
    
    profile = UserProfile.objects.get(user=request.user) 
    
    
    
    
    page = request.GET.get('page', 1)
    paginator = Paginator(order_itemz, 2)

    try:
        order_itemz = paginator.page(page)
    except PageNotAnInteger:
        order_itemz = paginator.page(1)
    except EmptyPage:
        order_itemz = paginator.page(paginator.num_pages)
    
    
    context = {
        'orders': orders,
        'profile': profile,
        'userproducts': userproducts,
        'order_items': order_items,
        'order_itemz': order_itemz,
        'categories': categories
    }
    
    return render(request, 'cowshare/usersprofile.html',context)


def products(request, category=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    for product in products:
        print('sharing number is', product.sharing_number)
    print("all products", products)
    if category:
        print(category)
        # category = get_object_or_404(Category, category)
        # print(category)
        category = Category.objects.get(name=category)
        products = Product.objects.filter(available=True,category=category)
        print(category, products)
        # products = products.filter(category=category)
        # print("category",products)
        
    
    
    




    print(products)
    context = {
        'categories': categories,
        'products':products, 
        'category':category
    }
    return render(request, 'cowshare/products.html',context)


def product_detail(request, pk):
    categories = Category.objects.all()
    product = get_object_or_404(Product, pk=pk, available=True)
    total = OrderItem.objects.filter(product=product,order__paid=True,order__verified=True).aggregate(Sum('quantity'))['quantity__sum']
    if not total:
        total = 0
    remaining_shares = product.sharing_number - total
    
    
    
    cart_product_form = CartAddProductForm()
    context = {
        'product':product,
        'cart_product_form':cart_product_form,
        'categories':categories,
        'remaining_shares': remaining_shares
    }
    return render(request, 'cowshare/productdetails.html',context)

@login_required
def user_order(request):
    # user_orders = Order.objects.filter(user=request.user)
    # print('user_orders',user_orders)
    user_orders = OrderItem.objects.filter(order__user=request.user).order_by('-order__created')
    print('all user orders:',user_orders)
    for user_order in user_orders:
        print('user order product name:',user_order.product.name)
        print('user order product name:',user_order.order.parts_to_exclude)
        if user_order.order.delivered:
            print('delivered')
        else:
            print('in progress')
    context = {
       'user_orders': user_orders, 
    }
    return render(request, 'cowshare/userprofilepage2.html',context)

@login_required
def usermessages(request):
    user_messages = Message.objects.filter(user=request.user).order_by('-created')
    for user_message in user_messages:
        print(user_message.user_message)
    context = {
        'user_messages': user_messages
    }
    return render(request, 'cowshare/usermessages.html',context)


@login_required
def send_email_verification(request):
    email_address = request.user.emailaddress_set.get(primary=True)
    email_confirmation = EmailConfirmationHMAC.from_email_address(email_address)
    send_email_confirmation(request, email_confirmation)
    return HttpResponseRedirect(reverse('home'))


def search(request):
    sendMessage = ""
    categories = Category.objects.all()
    try:
        if request.method == 'POST':
            category = request.POST.get('search')
            category = Category.objects.get(name__icontains=category)
            products = Product.objects.filter(category=category)
    except:
        products = Product.objects.all()  
        sendMessage = "Your search product does not exist"
    
    context = {
        'products' : products,
        'category' : category,
        'categories' : categories,
        'sendMessage' : sendMessage
    }
    return render(request, 'cowshare/products.html',context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        # email = request.POST.get('email')
        image_file = request.FILES.get('imagefile')
        user_data = CustomUser.objects.get(email=request.user.email)
        profile = UserProfile.objects.get(user=user_data)
        profile.firstname = firstname
        profile.lastname = lastname
        # user_data.email = email
        profile.profile_pic = image_file
        profile.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('cowshare:users-profile')

        
        



def exchangeoffer(request):
    context = {
        
    }
    return render(request, 'cowshare/exchangeoffer.html',context)

