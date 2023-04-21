# cowshare/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_images')
    
    def __str__(self):
        return self.user.email
class Category(models.Model):
    name = models.CharField(max_length=200)   
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]    
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=200)   
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]    
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'
        
    def __str__(self):
        return self.name

    
class Product(models.Model):
    category = models.ForeignKey(Category, 
                                 related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, 
                                 related_name='productsubcategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    sharing_price = models.DecimalField(max_digits=10,decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sharing_number = models.IntegerField()
    gender = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cowshare:productdetail',
                       args=[self.id])
        
        
class Message(models.Model):
    user = models.ForeignKey(CustomUser, related_name='messages', on_delete=models.CASCADE)
    user_message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Message for {self.user.email}'