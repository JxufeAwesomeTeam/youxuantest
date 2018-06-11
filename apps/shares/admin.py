from django.contrib import admin
from .models import Share

# Register your models here.
@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('id','user','book','share_text','like','share_time')
