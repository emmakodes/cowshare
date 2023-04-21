# cowshare/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Category, Product, SubCategory, UserProfile, Message

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated','gender']
    list_editable = ['price', 'available']
    

admin.site.register(UserProfile)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_message', 'created', 'updated']
    list_filter = ['created', 'updated']
