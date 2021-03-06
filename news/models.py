from django.db import models
from django.conf import settings
from django.urls import reverse

import re

source = (
    (1, "tvKlan"),
    (2, "Faxweb"),
    (3, "top-channel")
)
cat = (
    (1, "Politike"),
    (2, "Aktualitet"),
    (3, "Sport"),
    (4, "Lifestyle"),
    (5, "Rajoni"),
    (6, "Bota"),
    (7, "Teknologji"),
    (8, "Kuriozitet"),
    (9, "Kulture"),
    (10, "Kronike"),
    (11, "Te Tjera")
)
class Artikull(models.Model):
    
    img = models.TextField(blank=True,null = True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True,max_length=255)
    published = models.DateTimeField(auto_now_add=True, blank=True)
    video = models.BooleanField(default=False)
    nga = models.IntegerField(choices = source, default=1)
    categ = models.IntegerField(choices = cat, default=11)
    hits = models.IntegerField(default=0)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:article",kwargs={
            'slug':self.slug
        })
    def get_icon(self):
        e = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

        id = (e.match(self.img).group('id'))
        return ("https://img.youtube.com/vi/"+id+"/0.jpg")
class Comment(models.Model):
    artikull = models.ForeignKey(Artikull,on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE)
    con = models.CharField(max_length = 255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    postdate =  models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=1)

    def children (self):
        return Comment.objects.filter(parent= self)

    def __str__(self):
        return self.con