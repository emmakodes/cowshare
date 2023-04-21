from django.contrib import admin
from .models import Order, OrderItem, ExchangeOffer, ExchangeOfferResponse, Refund, Feedback, DeliveryCommpany
import csv
import datetime
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
              field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'



# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name',
                    'address', 'phone', 'postal_code', 'city',
                    'paid', 'state', 'created', 'updated', 'country',
                    'parts_to_exclude', 'delivery_company', 
                    'delivered', 'refund_requested', 'refund_granted']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


class ExchangeOfferResponseInline(admin.TabularInline):
    model = ExchangeOfferResponse
    raw_id_fields = ['order']
    
@admin.register(ExchangeOffer)

class ExchangeOfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'user', 'created', 'updated']
    list_filter = ['created', 'updated']
    inlines = [ExchangeOfferResponseInline]
    
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['reason', 'user', 'order',
                     'created', 'updated', 'granted']
    list_filter = ['created', 'updated', 'granted']
    # list_editable = ['price', 'available']
    
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'order',
                    'created', 'updated']
    list_filter = ['created', 'updated']
    
admin.site.register(DeliveryCommpany)



