from django.db import models
from cowshare.models import Product, CustomUser
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
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
        return self.price * self.quantity
    
class Refund(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    orderitem = models.ForeignKey(OrderItem, related_name='refunditems',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.orderitem.product.id
    
    
class Feedback(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    orderitem = models.ForeignKey(OrderItem, related_name='feedbackitems',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.orderitem.product.id
    
    
class ExchangeOffer(models.Model):
    message = models.CharField(max_length=500)
    orderitem = models.ForeignKey(OrderItem, related_name='exchangeitems',
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
    orderitem = models.ForeignKey(OrderItem, related_name='exchangeresponseitems',
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
        
        
class DeliveryCommpany(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name
    
class Delivery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deliverycompany = models.ForeignKey(DeliveryCommpany, related_name='delivery',
                              on_delete=models.CASCADE)
    orderitem = models.ForeignKey(OrderItem, related_name='deliveryitems',
                              on_delete=models.CASCADE) 
    delivered = models.BooleanField(default=False)
    
    def __str__(self):
        return  self.orderitem.product.id

  
class Exclusion(models.Model):
    description = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    orderitem = models.ForeignKey(OrderItem, related_name='exclusionitems',
                              on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.user.email
    
    
    
