from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.book.views import *


router = DefaultRouter()
# 默认使用model小写复数， base_name为小写单数
router.register(r'books', BookViewSet, base_name='books')
router.register(r'bookTypes',BookTypeViewSet,base_name='bookTypes')
urlpatterns = router.urls