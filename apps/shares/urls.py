from rest_framework.routers import DefaultRouter

from .views import BookShareViewSet
router = DefaultRouter(trailing_slash=True)

router.register(r'',BookShareViewSet,base_name='BookShare')

urlpatterns = router.urls
