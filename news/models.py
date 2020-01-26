from django.db import models
from django.conf import settings


class Artikull(models.Model):
    
    img = models.TextField(blank=True,null = True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    published = models.DateTimeField(auto_now_add=True, blank=True)
    video = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:article",kwargs={
            'slug':self.slug
        })
class Comment(models.Model):
    artikull = models.ForeignKey(Artikull,on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE)
    con = models.CharField(max_length = 255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    postdate =  models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.con