from django.db import models
from django.conf import settings

class Link (models.Model):
    link =  models.CharField(max_length=255)
    shorturl = models.CharField(blank= True, null=True,max_length=150)
    vi = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)   
    def __str__(self):
        return self.link
