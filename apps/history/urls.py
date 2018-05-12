from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.history.views import BookHistoryViewSet


router = DefaultRouter(trailing_slash=True)
# 默认使用model小写复数， base_name为小写单数
router.register(r'', BookHistoryViewSet, base_name='bookHistory')

urlpatterns = router.urls