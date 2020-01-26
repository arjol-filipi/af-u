from django.shortcuts import render

from django.views.generic import TemplateView

app_name = 'core'

class Home(TemplateView):
    template_name = 'home.html'
