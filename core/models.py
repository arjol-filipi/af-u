from django.db import models


class Extra(models.Model):
    name = models.CharField(max_length= 100)
    live_Url = models.TextField(default=' ')
    des = models.TextField(default=' ')
    code_url = models.TextField(default=' ')
    background = models.CharField(max_length= 250)
    pos = models.IntegerField(default=4)
    def __str__(self):
        return str( self.name)