from ..models import Artikull
from .serializer import ArticleSerializer
from django.db.models import Q
from rest_framework import viewsets

ak = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    paginate_by = 20
    def get_queryset(self):
        q = None
        try:
            q=(self.request.META['HTTP_Q'])
        except:
            pass
        rk=(self.request.META['HTTP_X_KEY'])
        if ak!=rk:
            queryset = Artikull.objects.none()
        elif not q:
            queryset = Artikull.objects.all()
        else:
            queryset = Artikull.objects.filter(
                Q(title__icontains=q)|Q(content__icontains=q)
            )
        return queryset.order_by('-published')

        