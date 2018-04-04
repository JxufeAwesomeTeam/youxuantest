from django.db import models

# Create your models here.
class User(models.Model):
    '''
    用户名，邮箱，密码
    '''
    gender = (
        ('male','男'),
        ('female','女')
    )

    username = models.CharField(max_length=20,unique=True,verbose_name='用户名')
    password = models.CharField(max_length=20,verbose_name='密码')
    #icon = models.ImageField(upload_to='user_icon',default='user_icon/default.jpg',verbose_name='头像')
    email = models.EmailField(unique=True,verbose_name='邮箱')
    sex = models.CharField(max_length=32,choices=gender,default='男',verbose_name='性別')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'