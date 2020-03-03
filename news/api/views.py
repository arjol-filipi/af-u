from ..models import Artikull
from .serializer import ArticleSerializer

from rest_framework import viewsets

ak = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    paginate_by = 20
    def get_queryset(self):
        rk=(self.request.META['HTTP_X_KEY'])
        if ak!=rk:
            queryset = Artikull.objects.none()
        else:
            queryset = Artikull.objects.all().order_by('-published')
        return queryset