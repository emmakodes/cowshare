from django.urls import path
from . import views

app_name = 'cowshare'

urlpatterns = [
    path('', views.index, name='index'),
    path('send-email-verification/', views.send_email_verification, name='send_email_verification'),
    path('profile/', views.profile, name='users-profile'),
    path('products/', views.products, name='allproducts'),
    path('products/<str:category>/', views.products, name='productscategory'),
    path('productdetail/<int:pk>', views.product_detail, name='productdetail'),
    path('userorder/', views.user_order, name='userorder'),
    path('exchangeoffer/', views.exchangeoffer, name='exchangeoffer'),
    path('usermessages/', views.usermessages, name='usermessages'),
    path('search/', views.search, name='searchProducts'),
    path('updateprofile', views.update_profile, name='update_profile'),
]