from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.login.models import User
from apps.book.models import ISBNBook
# Create your models here.

class History(models.Model):
    book = models.ForeignKey(ISBNBook,on_delete=models.DO_NOTHING,verbose_name='访问书籍')
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='访问用户')
    visit_time = models.DateTimeField(auto_now=True,verbose_name='访问时间')  #重复访问会更新时间

    class Meta:
        ordering = ['id']
        verbose_name = '访问记录'
        verbose_name_plural = '访问记录'