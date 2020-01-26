from django.urls import path
from django.conf.urls import url

from .views import News,Article,scrappTop

app_name = "news"

urlpatterns = [
    path('news/', News.as_view(), name='news'),
    path('news/<slug>/', Article.as_view(), name='article'),
    path('news/scrapetop', scrappTop, name='scrapetop'),
    ]