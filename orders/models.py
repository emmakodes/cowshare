from django.db import models
from cowshare.models import Product, CustomUser
from django.utils import timezone
import secrets
from .paystack  import  Paystack
# Create your models here.

class DeliveryCommpany(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    
    class Meta:  
        verbose_name = 'DeliveryCompany'
        verbose_name_plural = 'DeliveryCompanies'
    
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200, default="Nigeria")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    parts_to_exclude = models.TextField(blank=True)
    exchange_offer = models.TextField(blank=True)
    exchange_offer_request_status = models.BooleanField(default=False)
    delivery_company = models.ForeignKey(DeliveryCommpany, on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return f'{self.user.email}'
        # return f'Order {self.id}'
    
    # def get_total_cost(self):
    #     return sum(item.get_cost() for item in self.items.all())
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        print('order total cost',total_cost)
        return total_cost
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Order.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)
      
        
    # def amount_value(self):
    #     return int(self.get_total_cost) * 100
    def amount_value(self):
        value = self.get_total_cost()
        return int(value) * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.get_total_cost)
        print('verify payment amount',result['amount'])
        if status:
            if result['amount'] / 100 == self.get_total_cost():
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        print('orderitem total cost', self.price * self.quantity)
        return self.price * self.quantity
    
    
    
class Refund(models.Model):
    reason = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='refundorder',
                              on_delete=models.SET_NULL, blank=True, null=True)
    granted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Refund for order {self.order.id}'

    
    
class Feedback(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='feedbacks',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Feedback for order {self.order.id}'

    
    
class ExchangeOffer(models.Model):
    message = models.CharField(max_length=500)
    order = models.ForeignKey(Order, related_name='exchangeoffer',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email
    
class ExchangeOfferResponse(models.Model):
    message = models.CharField(max_length=500)
    exchangeoffer = models.ForeignKey(ExchangeOffer, related_name='exchangeoffer',
                              on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='exchangeofferresponse',
                              on_delete=models.CASCADE)   
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email
    
    
# class count(models.Model):
#     number = models.PositiveIntegerField(default=0)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     orderitem = models.ForeignKey(OrderItem, related_name='items',
#                               on_delete=models.CASCADE)  
#     product = models.ForeignKey(Product, related_name='products',
#                                 on_delete=models.CASCADE)
        
        

    
# class Delivery(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     deliverycompany = models.ForeignKey(DeliveryCommpany, related_name='delivery',
#                               on_delete=models.CASCADE)
#     orderitem = models.ForeignKey(OrderItem, related_name='deliveryitems',
#                               on_delete=models.CASCADE) 
#     delivered = models.BooleanField(default=False)
    
#     def __str__(self):
#         return  self.orderitem.product.id

  
# class Exclusion(models.Model):
#     description = models.CharField(max_length=500)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     orderitem = models.ForeignKey(OrderItem, related_name='exclusionitems',
#                               on_delete=models.CASCADE) 
    
#     def __str__(self):
#         return self.user.email
    
    
    
