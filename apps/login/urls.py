from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.login.views import *


router = DefaultRouter()
# 默认使用model小写复数， base_name为小写单数
router.register(r'users', UserViewSet, base_name='user')
urlpatterns = router.urls