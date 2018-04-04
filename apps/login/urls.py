from django.urls import path
from apps.login.views import *

urlpatterns = [
    path('',user_list),
    path('/<int:pk>',user_detail),
    path('login',login),
]
