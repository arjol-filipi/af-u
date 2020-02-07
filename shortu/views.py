from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponsePermanentRedirect,HttpResponseRedirect
from django.db.models import Count

from .forms import UrlForm
from .models import Link

import random
import string

def short_url_gen(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))
@require_GET
def Follow(request,shorturl):
    link = get_object_or_404(Link,shorturl=shorturl)
    link.vi += 1
    print(link.vi)
    link.save()
    return HttpResponseRedirect(link.link)

def FormView(request):
    toplink = Link.objects.annotate(Count('vi')).order_by('-vi__count')[:5]
    if request.user.is_authenticated:
        yl = Link.objects.filter(user = request.user)
    else:
        yl = None
    context = {
        'form' :UrlForm,
        'links':yl,
        't':toplink
    }

    return render(request, 'shortu.html', context)
@require_GET
def info(request,shorturl):
    link = get_object_or_404(Link,shorturl=shorturl)
    return render(request,'info.html',{'link':link})

@require_POST
def Submit(request):
    form = UrlForm(request.POST)
    if form.is_valid():
        link = form.cleaned_data['url']
        costom = form.cleaned_data['costom']
        if costom:
            if Link.objects.filter(shorturl=costom).exists():
                #messages(request,"Costom url aready taken")
                pass
            else: 
                shorturl = costom
                newlink = Link.objects.create(link= link,user = request.user, shorturl= shorturl)
                return render(request,'info.html',{'link':newlink})
        j=1
        while j<11:
            newshort = short_url_gen(j)
            if Link.objects.filter(shorturl=costom).exists():
                j+=1
                continue
            newlink = Link.objects.create(link= link, shorturl= newshort,user = request.user)
            return render(request,'info.html',{'link':newlink})
            

    return render(request, 'home.html')