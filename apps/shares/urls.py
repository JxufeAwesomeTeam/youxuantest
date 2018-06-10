from rest_framework.routers import DefaultRouter

from .views import BookShareViewSet
router = DefaultRouter()

router.register(r'shares',BookShareViewSet,base_name='share')
