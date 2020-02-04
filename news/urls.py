from django.urls import path
from django.conf.urls import url

from .views import News,Article,CommentView,ReplyView,SearchView,Save_Art

app_name = "news"

urlpatterns = [
    path('news/', News.as_view(), name='news'),
    path('news/<slug>/', Article.as_view(), name='article'),
    path('news/comment/<slug>', CommentView, name='comment'),
    path('news/reply/<id>', ReplyView, name='reply'),
    path('news/add/', Save_Art, name='add'),
    path('search/',SearchView.as_view(),name='search'),
    ]