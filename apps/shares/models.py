from django.db import models

from apps.book.models import Book
from apps.login.models import User

# Create your models here.
class Share(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, verbose_name='分享书籍')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='分享用户')
    share_time = models.DateTimeField(auto_now=True,verbose_name='分享时间')
    share_text = models.CharField(max_length=200,verbose_name='分享词')
    like = models.IntegerField(default=0,verbose_name='点赞数')
