from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
    list_display = ('id','typename')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title','price','url','loc','review','photo',)
    # filter_horizontal = ('typename',)