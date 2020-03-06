from django.urls import path
from django.conf.urls import url,include
from .views import News,Article,CommentView,ReplyView,SearchView,Save_Art,scrappTop,scrappF
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from .api.views import ArticleViewSet
router = routers.DefaultRouter()
router.register(r'article-list',ArticleViewSet,'article-list')

app_name = "news"

urlpatterns = [
    path('news/', News.as_view(), name='news'),
    path('news/<slug>/', Article.as_view(), name='article'),
    path('news/comment/<slug>', CommentView, name='comment'),
    path('news/reply/<id>', ReplyView, name='reply'),
    path('new/add/', csrf_exempt(Save_Art), name='add'),
    path('search/',SearchView.as_view(),name='search'),
        path('new/test',scrappTop,name='st'),
        path('new/test2',scrappF,name='sf'),
        path('api/', include(router.urls))
    ]