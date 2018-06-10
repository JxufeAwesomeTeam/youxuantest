from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.
class User(models.Model):
    '''
    用户名，邮箱，密码
    '''
    gender = (
        ('male', '男'),
        ('female', '女')
    )

    username = models.CharField(max_length=100,verbose_name='用户名')
    password = models.CharField(max_length=100,verbose_name='密码')
    email = models.EmailField(max_length=30,verbose_name='邮箱')
    sex = models.CharField(max_length=32, choices=gender, default='男', verbose_name='性別')
    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = '用户'
        verbose_name_plural = '用户'
