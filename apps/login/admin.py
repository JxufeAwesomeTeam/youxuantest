from django.contrib import admin
from .models import User
# Token

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','password','email','sex','created_time')


# @admin.register(Token)
# class TokenAdmin(admin.ModelAdmin):
#     list_display = ('key','user','created')
