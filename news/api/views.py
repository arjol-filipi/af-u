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
        c=None
        try:
            c=self.request.META['HTTP_C']
            c = [int(ca) for ca in c.split(',')  ]
        except:
            pass
        print(type(c))
        s=None
        try:
            s=self.request.META['HTTP_S']
            s = [int(sa) for sa in s.split(',')  ]
        except:
            pass
        try:
            q=(self.request.META['HTTP_Q'])
        except:
            pass
        
        rk=(self.request.META['HTTP_X_KEY'])
        if ak!=rk:
            queryset = Artikull.objects.none()
        else:
            queryset = Artikull.objects.all()
        if c:
            queryset = Artikull.objects.filter(categ__in=c)
        if s:
            queryset = Artikull.objects.filter(nga__in=s)
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)|Q(content__icontains=q)
            )
            
        
        return queryset.order_by('-published')

        