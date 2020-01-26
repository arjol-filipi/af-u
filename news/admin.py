from django.contrib import admin

from .models import Artikull
class ArtikullAdmin(admin.ModelAdmin):
    list_display = ['title','published']

admin.site.register(Artikull,ArtikullAdmin)