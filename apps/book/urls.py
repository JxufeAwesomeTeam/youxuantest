from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.book.views import *

from .cache import get_book_pv,set_book_pv

router = DefaultRouter()
# 默认使用model小写复数， base_name为小写单数
router.register(r'books', BookViewSet, base_name='book')
router.register(r'bookTypes',BookTypeViewSet,base_name='bookType')
router.register(r'ISBNbooks',ISBNBookViewSet,base_name='ISBNbook')
urlpatterns = [
    path(r'pvRank/',get_book_pv),
    path(r'click/',set_book_pv),
]
urlpatterns +=router.urls