from django.urls import path
from django.conf.urls import url

from .views import FormView,Submit,Follow,info

app_name = "shortu"

urlpatterns = [
    path('shortu/', FormView, name='form-view'),
    path('shortu/url/',Submit,name='submit'), 
    path('s/<shorturl>/',Follow,name='follow'),
    path('shortu/<shorturl>',info,name='info'),
     ]
    