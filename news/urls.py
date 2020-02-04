from django.urls import path
from django.conf.urls import url

from .views import News,Article,CommentView,ReplyView,SearchView,Save_Art,scrappTop
from django.views.decorators.csrf import csrf_exempt
app_name = "news"

urlpatterns = [
    path('news/', News.as_view(), name='news'),
    path('news/<slug>/', Article.as_view(), name='article'),
    path('news/comment/<slug>', CommentView, name='comment'),
    path('news/reply/<id>', ReplyView, name='reply'),
    path('new/add/', csrf_exempt(Save_Art), name='add'),
    path('search/',SearchView.as_view(),name='search'),
        path('news/test',scrappTop,name='st'),
    ]