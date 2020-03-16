from django.contrib import admin
from datetime import datetime,timedelta
from .models import Artikull,Comment
class AgeFilter(admin.SimpleListFilter):
    title = "Post age"
    parameter_name = 'published'
    def lookups(self, request, model_admin):
        return (
          ('new', ('Last month')),
          ('old', ('Older than a month')),
       )
    def queryset(self, request, queryset):
         
        if self.value() == 'new':
            return queryset.filter(published__gte=datetime.now()-timedelta(days=30))
        elif self.value() == 'old':
            return queryset.filter(published__lt=datetime.now()-timedelta(days=30))
        else:
            return queryset

class ArtikullAdmin(admin.ModelAdmin):
    list_display = ['title','published','nga','categ']
    list_filter = (AgeFilter,)
admin.site.register(Artikull,ArtikullAdmin)

admin.site.register(Comment)