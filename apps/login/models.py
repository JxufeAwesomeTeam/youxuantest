from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    '''
    用户名，邮箱，密码
    '''
    gender = (
        ('male', '男'),
        ('female', '女')
    )

    # icon = models.ImageField(upload_to='user_icon',default='user_icon/default.jpg',verbose_name='头像')
    sex = models.CharField(max_length=32, choices=gender, default='男', verbose_name='性別')

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = '用户'
        verbose_name_plural = '用户'
