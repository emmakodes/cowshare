from django.urls import path
from . import views

app_name = 'cowshare'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products')
]