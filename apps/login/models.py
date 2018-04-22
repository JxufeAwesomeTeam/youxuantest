import binascii

import os
from django.db import models


# Create your models here.
class User(models.Model):
    '''
    用户名，邮箱，密码
    '''
    gender = (
        ('male', '男'),
        ('female', '女')
    )

    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    # icon = models.ImageField(upload_to='user_icon',default='user_icon/default.jpg',verbose_name='头像')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    sex = models.CharField(max_length=32, choices=gender, default='男', verbose_name='性別')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


# class Token(models.Model):
#     """
#     The default authorization token model.
#     """
#     key = models.CharField("Key", max_length=40, primary_key=True)
#     user = models.OneToOneField(
#         User, related_name='auth_token',
#         on_delete=models.CASCADE, verbose_name="User"
#     )
#     created = models.DateTimeField("Created", auto_now_add=True)
#
#     class Meta:
#         verbose_name = "Token"
#         verbose_name_plural = "Tokens"
#
#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super(Token, self).save(*args, **kwargs)
#
#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()
#
#     def __str__(self):
#         return self.key
#
#
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)