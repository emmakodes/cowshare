from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
    path('exclusions/<str:exref>', views.exclusions, name='exclusions'),
]