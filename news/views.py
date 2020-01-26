from django.shortcuts import render
from django.views.generic import ListView,DetailView
#scrap
from bs4 import BeautifulSoup
import requests,re
from django.utils.text import slugify


from .models import Artikull
class News(ListView):
    queryset = Artikull.objects.order_by('-published')
    template_name = 'news.html'

class Article(DetailView):
    model = Artikull
    template_name = 'article.html'
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