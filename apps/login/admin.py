from django.contrib import admin
from .models import User
# Token

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','password','email','sex','date_joined')


# @admin.register(Token)
# class TokenAdmin(admin.ModelAdmin):
#     list_display = ('key','user','created')
