from bs4 import BeautifulSoup
import requests,re
# from news.models import Artikull
from django.utils.text import slugify
from datetime import datetime,timedelta
import urllib.request
import json      


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)





def scrappTop():
    session = requests.Session()
    session.cookies.set(name='__cfduid',value='d87cb1de0b6841d489058006895a1f6f41583323041')
    session.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    url = "http://top-channel.tv/artikuj/te-fundit/"
    content = session.get(url,verify= False).content
    soup = BeautifulSoup(content,"html.parser")
    print(content)
    del(content)
    art = soup.find_all('div',attrs={'class':"articles"})
    
    del(soup)
    
    divs = art[0].find_all('div',attrs={'class':"article sub col-xs-12 col-sm-12 col-md-12 col-lg-12"})
    
    
    for div in divs:
        links = div.find_all('a',attrs={'class':"articleLink",'href': re.compile("^http://")})
        for link in links:
            
            url = (link.get('href'))
            print(url)
            ar = session.get(url,verify= False).content
            p = BeautifulSoup(ar,"html.parser")
            title = p.find_all('div',attrs={'class':"inner titleInner"})
            title = p.find_all('h1')[0].text
            

            i=p.find_all('img',attrs={'class':"img-responsive fullWidthImage articleImage"})
            if i:
                img = i[0].get('src')
            else:
                img = None
            con = p.find_all('div',attrs={'class':"articleContent"})
            
            try:
                con[0]
            except IndexError: 
                continue
            try:
                title[0]
            except IndexError:
                continue
            content = str(con[0])
            body= {
            'title':title,
            'content':content,
            'img':img
            }
            
            myurl = "https://af-u.herokuapp.com/new/add/"
            req = urllib.request.Request(myurl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            jsondata = json.dumps(body)
            jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
            req.add_header('Content-Length', len(jsondataasbytes))
            response = urllib.request.urlopen(req, jsondataasbytes)

def scrappKlan():
    res = {}
    us=0
    session = requests.Session()
    session.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    url = "https://tvklan.al/arkiva/"
    content = session.get(url,verify= False).content
    soup = BeautifulSoup(content,"html.parser")
    art = soup.find_all('div',attrs={'class':"tab-pane fade show active"})
    
    divs = art[0].find_all('article',attrs={'class':"tab-news-box"})
    
    
    for div in divs:
        
        links = div.find_all('a')
        for link in links:
            us+=1
            url = (link.get('href'))
            res[us]=  url
            
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
            con = main.find_all('p', text=re.compile("."))
           
            try:
                con[0]
            except IndexError: 
                continue
            try:
                title[0]
            except IndexError:
                continue
            content ="".join( str(c) for c in con)
            body ={
            'title':title,
            'content':content,
            'img':img}
            if video:
                body['video'] = True
            myurl = "https://af-u.herokuapp.com/new/add/"
            req = urllib.request.Request(myurl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            jsondata = json.dumps(body)
            jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
            req.add_header('Content-Length', len(jsondataasbytes))
            
            response = urllib.request.urlopen(req, jsondataasbytes)
    return res

def scrappFax():
    res = {}
    us=0
    session = requests.Session()
    session.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    base_url = 'https://www.faxweb.al/feed/'
    content = session.get(base_url,verify= False).text
    
    reg_fax = '(?<=k>https://www.faxweb.al/)(.*)(?=<)'
    li = re.findall(reg_fax,content)
    
    for link in li:
            us+=1
            url = 'https://www.faxweb.al/'+link
            
            res[us]=  url
            ar = session.get(url,verify= False).content
            p = BeautifulSoup(ar,"html.parser")
            title = p.find_all('h1',attrs={'class':"post-title entry-title"})
            title = p.find_all('h1')[0].text
            img = p.find('img',attrs={'class':"attachment-jannah-image-post size-jannah-image-post lazy-img wp-post-image"})
            iframe = p.find('iframe')
            video = False
            if img:
                img = img.get('data-src')
            else:
                video = True
                img = iframe.get('src')
            main = p.find('div',attrs={'class':"entry-content entry clearfix"})
            con = main.find_all('p')
            
            print(url)
            content ="".join( str(c) for c in con)
            body ={
            'title':title,
            'content':content,
            'img':img}
            if video:
                body['video'] = True
            myurl = "https://af-u.herokuapp.com/new/add/"
            req = urllib.request.Request(myurl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            jsondata = json.dumps(body)
            jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
            req.add_header('Content-Length', len(jsondataasbytes))
            
            response = urllib.request.urlopen(req, jsondataasbytes)
    return res
    # print(res)    
# scrappFax()
# scrappKlan()

# scrappTop()