from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .forms import CommentForm,ReplyForm
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponseRedirect
from django.db.models import Q
#scrap
from bs4 import BeautifulSoup
import requests,re
from django.utils.text import slugify


from .models import Artikull,Comment

def Save_Art(request):
    data = json.loads(request.body)
    print(data)
    title = data.get('title', None)
    content = data.get('content', None)
    img = data.get('img', None)
    slug  = create_slug(title)
    video = data.get('video', None)
    qs = Artikull.objects.filter(title=title)
    exists = qs.exists()
    if not exists:
        Article.object.create(title=tile,content=content,img=img,slug=slug,video=video)
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
    session = requests.Session()
    session.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    url = "https://tvklan.al/arkiva/"
    content = session.get(url,verify= False).content
    soup = BeautifulSoup(content,"html.parser")
    art = soup.find_all('div',attrs={'class':"tab-pane fade show active"})
    # print(art)
    divs = art[0].find_all('article',attrs={'class':"tab-news-box"})
    # print(divs)
    
    for div in divs:
        
        links = div.find_all('a')
        for link in links:
            url = (link.get('href'))
            ar = session.get(url,verify= False).content
            p = BeautifulSoup(ar,"html.parser")
            title = p.find_all('div',attrs={'class':"col-lg-8 col-12 readmore-title"})
            title = p.find_all('h1')[0].text
            
            ifig = p.find_all('figure',attrs={'class':"main_img single-lajme-main-img"})
            
            i=ifig[0].find('img')
            video = False
            if i is None:
                i=ifig[0].find('iframe')
                video = True
            
            try:
                img = i.get('src')
            except:
                img = None
            
            main = p.find('main')
            con = main.find_all('p')
            slug = create_slug(title)
            try:
                con[0]
            except IndexError: 
                continue
            try:
                title[0]
            except IndexError:
                continue
            qs = Artikull.objects.filter(title=title)
            exists = qs.exists()
            if not exists:
                new_a = Artikull()
                new_a.title=title
                new_a.content=str(con)
                new_a.img=img
                if video:
                    new_a.video = True
                new_a.slug=slug
                new_a.save()
    return render(request, 'home.html')