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
    # session = requests.Session()
    # session.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    
    url = "http://top-channel.tv/app/home.php"
    page = requests.get(url)
    
    res = page.json()
    
    
    for ar in res:
        
        # return res
        title = ar['title']
        if ar['videoID']:
            video = True
            img = 'https://www.youtube.com/embed/'+ar['videoID']
        else:
            img = img= ar["image"]
            video = False
        cat = ar['category']
        content = ar['content']
        if ar['galleryID']:
            for im in ar["galleryImages"]:
                content += "<img src="+im['url']+'>'
        body= {
        'title':title,
        'content':content,
        'img':img,
        'video':video,
        'cat':cat,
        's':'top-channel'
        }
        
        # # myurl = "https://af-u.herokuapp.com/new/add/"
        myurl = "http://127.0.0.1:8000/new/add/"
        req = urllib.request.Request(myurl)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))
        response = urllib.request.urlopen(req, jsondataasbytes)
    return res
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
        cat = div.find('span',attrs={'class':"categ"})
        print(cat.text)
        # if cat not in cat_c:
        #     cat = ''
        links = div.find_all('a')
        for link in links:
            us+=1
            url = (link.get('href'))
            res[us]=  [url,cat.text]
            
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
            'img':img,
            's':'tvKlan',
            'cat':cat.text
            }
            if video:
                body['video'] = True
            # myurl = "https://af-u.herokuapp.com/new/add/"
            myurl = "http://127.0.0.1:8000/new/add/"
            req = urllib.request.Request(myurl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            jsondata = json.dumps(body)
            jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
            req.add_header('Content-Length', len(jsondataasbytes))
            
            response = urllib.request.urlopen(req, jsondataasbytes)
    return res
cat_c = ["Politikë","Aktualitet", "Sport","Lifestyle","Rajoni","Bota","Teknologji", "Kuriozitet","Kulturë",
    "Kronikë"]
def scrappFax():
    res = {}
    us=0
    session = requests.Session()
    session.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    base_url = 'https://www.faxweb.al/feed/'
    content = session.get(base_url,verify= False).text
    # soup = BeautifulSoup(content,"xml")
    # return({0:content})
    item_reg ="</item>"
    reg_fax = '(?<=k>https://www.faxweb.al/)(.*)(?=<)'
    cat_reg ='(?<=<category><!\[CDATA\[)(.*)(?=\]\])'
    li = re.split(item_reg,content,re.MULTILINE)
    
    for item in li:
        # print(item)
        us+=1
        cats = re.findall(cat_reg,item)
        cat=''
        for pc in cats:
            if pc in cat_c:
                cat=pc
        link = re.findall(reg_fax,item)
        url = 'https://www.faxweb.al/'+link[0]
        # print(link)
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
        
        
        content ="".join( str(c) for c in con)
        body ={
        'title':title,
        'content':content,
        'img':img,
        's':'Faxweb',
        'cat':cat
        }
        if video:
            body['video'] = True
        # myurl = "https://af-u.herokuapp.com/new/add/"
        myurl = "http://127.0.0.1:8000/new/add/"
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