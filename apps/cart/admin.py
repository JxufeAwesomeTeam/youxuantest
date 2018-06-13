
from django.contrib import admin
from .models import CartItem
# Token

# Register your models here.
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','user','book')
