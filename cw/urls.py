from django.urls import path
from django.conf.urls import url

from .views import Load,Create,Main,Save,ListCross,Play

app_name = "cw"

urlpatterns = [
    path('cw/load', Load, name='load'),
    path('cw/create', Create, name='create'),
    path('cw/', Main, name='Main'),
    path('cw/save', Save, name='Save'),
    path('cw/all', ListCross.as_view(), name='list'),
    path('cw/play/<pk>', Play.as_view(), name='play'),
    ]