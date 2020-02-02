from django.db import models
from django.conf import settings

class Ans(models.Model):
    word = models.CharField(max_length=255)
    length = models.IntegerField(default=len(str(word)))
    popularity = models.IntegerField(default=1)
    used = models.IntegerField(default=1)
    solved =  models.IntegerField(default=1)
    hint = models.CharField(max_length=255)

    def __str__(self):
        return self.word
    def get_hints(self):
        return set(self.hint.split("-_-"))

class CrossWord(models.Model):
    board = models.TextField(default=' ')
    published = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return str( self.id)
class Lead(models.Model):
    i = models.IntegerField(default=0)
    j = models.IntegerField(default=0)
    crosword = models.ForeignKey(CrossWord,on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True) 
    orientation = models.CharField(max_length=1)
    word = models.CharField(max_length=30)
    hint = models.CharField(max_length=255)
    pos = models.CharField(max_length= 3)
    def get_hint(self):
        return str(self.hint.split("-_-")[0])
    def int_post(self):
        return int(self.pos)+1
    def __str__(self):
        return self.word