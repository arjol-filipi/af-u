from django.contrib import admin

from .models import Artikull,Comment
class ArtikullAdmin(admin.ModelAdmin):
    list_display = ['title','published']

admin.site.register(Artikull,ArtikullAdmin)

admin.site.register(Comment)