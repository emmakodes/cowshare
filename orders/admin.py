from django.contrib import admin
from .models import Order, OrderItem, ExchangeOffer, ExchangeOfferResponse, Exclusion, Refund, Feedback, Delivery, DeliveryCommpany

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name',
                    'address', 'phone', 'postal_code', 'city',
                    'paid', 'state', 'created', 'updated', 'country']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


class ExchangeOfferResponseInline(admin.TabularInline):
    model = ExchangeOfferResponse
    raw_id_fields = ['orderitem']
    
@admin.register(ExchangeOffer)

class ExchangeOfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'user', 'created', 'updated']
    list_filter = ['created', 'updated']
    inlines = [ExchangeOfferResponseInline]
    
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'orderitem',
                     'created', 'updated']
    list_filter = ['created', 'updated']
    # list_editable = ['price', 'available']
    
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'orderitem',
                    'created', 'updated']
    list_filter = ['created', 'updated']
    
admin.site.register(DeliveryCommpany)

admin.site.register(Delivery)

admin.site.register(Exclusion)


