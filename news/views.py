from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .forms import CommentForm,ReplyForm
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.db.models import Q
#scrap

import requests,re
from django.utils.text import slugify

from news.sc import scrappKlan as sk
from news.sc import scrappFax as sf
from .models import Artikull,Comment
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def Save_Art(request):
    print("at here")
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        title = data.get('title', None)
        content = data.get('content', None)
        img = data.get('img', None)
        slug  = create_slug(title)
        video = data.get('video', None)
        if video:
            video = True
        else:
            video = False
        qs = Artikull.objects.filter(title=title)
        exists = qs.exists()
        if not exists:
            a = Artikull.objects.create(title=title,content=content,img=img,slug=slug,video=video)
            return HttpResponseRedirect(a.get_absolute_url())    
        return HttpResponseRedirect(qs[0].get_absolute_url())
class News(ListView):
    queryset = Artikull.objects.order_by('-published')
    paginate_by = 12
    template_name = 'news.html'
    def get_context_data(self,**kwargs):
        context = super(News,self).get_context_data(**kwargs)
        
        context['sq'] = None       
        return context

class Article(DetailView):
    model = Artikull
    template_name = 'article.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        context['form'] = CommentForm
        context['reply'] = ReplyForm
        return context
class SearchView(ListView):
    template_name = 'news.html'
    
    paginate_by = 12
    def get_context_data(self,**kwargs):
        context = super(SearchView,self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['sq'] = query        
        return context
    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        object_list = Artikull.objects.filter(
                Q(title__icontains=query)|Q(content__icontains=query)
            )
        return object_list.order_by('-published')


@require_POST
def CommentView(request,slug):
    form = CommentForm(request.POST)
    artikull = Artikull.objects.filter(slug = slug)
    if form.is_valid():
        content = form.cleaned_data['comment']
        user = request.user
        
        new_comment = Comment.objects.create(user=user,artikull=artikull[0],con=content)

    
    return HttpResponseRedirect(artikull[0].get_absolute_url())
@require_POST
def ReplyView(request,id):
    parent = Comment.objects.filter(id= id)
    if parent.exists():
        parent = parent[0]
        form = ReplyForm(request.POST)
        if form.is_valid():
            con = form.cleaned_data['reply']
            user = request.user
            level = parent.level + 1
            if level > 3:
                parent = parent.parent
                level = 3
            new_reply = Comment.objects.create(user= user,parent=parent,con=con,level = level,artikull=parent.artikull)
            return HttpResponseRedirect(parent.artikull.get_absolute_url())
    return HttpResponseRedirect('/')

def create_slug(title, new_slug=None):
        slug = slugify(title, allow_unicode = True)
        if new_slug is not None:
            slug = new_slug
        qs = Artikull.objects.filter(slug=slug).order_by("-id")
        exists = qs.exists()
        if exists:
            new_slug = "%s-%s"%(slug, qs.first().id)
            return create_slug(title, new_slug=new_slug)
        return slug

def scrappTop(request):
    print('ddsdfsdfds')
    # st()
    res = sk()

    return JsonResponse(res) 
def scrappF(request):
    print('ddsdfsdfds')
    # st()
    res = sf()

    return JsonResponse(res) 