from bs4 import BeautifulSoup
import requests,re
# from news.models import Artikull
from django.utils.text import slugify
from datetime import datetime,timedelta

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def deleteOld():
    Artikull.objects.filter(published__lte=datetime.now()-timedelta(days=30)).delete()
    print("deleted old artikull")

def scrappTop():
    session = requests.Session()
    session.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    url = "http://top-channel.tv/artikuj/te-fundit/"
    content = session.get(url,verify= False).content
    soup = BeautifulSoup(content,"html.parser")
    art = soup.find_all('div',attrs={'class':"articles"})
    divs = art[0].find_all('div',attrs={'class':"article sub col-xs-12 col-sm-12 col-md-12 col-lg-12"})
    # print(divs[1])
    
    for div in divs:
        links = div.find_all('a',attrs={'class':"articleLink",'href': re.compile("^http://")})
        for link in links:
            url = (link.get('href'))
            ar = session.get(url,verify= False).content
            p = BeautifulSoup(ar,"html.parser")
            title = p.find_all('div',attrs={'class':"inner titleInner"})
            title = p.find_all('h1')[0].text
            print(title)

            i=p.find_all('img',attrs={'class':"img-responsive fullWidthImage articleImage"})
            if i:
                img = i[0].get('src')
            else:
                img = None
            con = p.find_all('div',attrs={'class':"articleContent"})
            slug = create_slug(title)
            try:
                con[1]
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
                new_a.content=str(con[0])
                new_a.img=img
                new_a.slug=slug
                new_a.save()

def scrappKlan():
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
                new_a.content="".join(con)
                new_a.img=img
                if video:
                    new_a.video = True
                new_a.slug=slug
                new_a.save()
scrappKlan()