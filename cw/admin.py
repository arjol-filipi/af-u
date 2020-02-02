from django.contrib import admin

from .models import Ans,CrossWord,Lead

class AnsAdmin(admin.ModelAdmin):
    ordering = ('word',)

admin.site.register(Ans,AnsAdmin)
admin.site.register(CrossWord)
admin.site.register(Lead)
