from django.urls import path
from .views import *

urlpatterns = (
    path('',Spider),
    path('JD',JDSpiderView,name='JD'),
    path('DD',DDSpiderView,name='DD'),
    path('TB',TBSpiderView,name='TB'),
)