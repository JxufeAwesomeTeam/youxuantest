from django.urls import path
from .views import *

urlpatterns = (
    path('',Spider),
    path(r'JD/<int:page>',JDSpiderView,name='JD'),
    path(r'DD/<int:page>',DDSpiderView,name='DD'),
    path(r'TB/<int:page>',TBSpiderView,name='TB'),
    path(r'union',UnionISBN)
)