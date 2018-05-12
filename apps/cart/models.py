from django.db import models
# Create your models here.

from apps.book.models import Book
from apps.login.models import User

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name='书籍id')
    quantity = models.IntegerField(default=1,verbose_name='数量')

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = "购物车"



