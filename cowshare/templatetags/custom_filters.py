from django import template
from django.db.models import Sum
from orders.models import OrderItem

register = template.Library()

@register.filter
def total_orders(product):
    total = OrderItem.objects.filter(product=product,order__paid=True,order__verified=True).aggregate(Sum('quantity'))['quantity__sum']
    print("total is", total)
    return total if total else 0


# {% load custom_filters %}
# {{ product|total_orders }}