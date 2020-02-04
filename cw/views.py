from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Ans,CrossWord,Lead
from django.db.models import F
# json
from django import db
from django.http.response import HttpResponse
import json
import os
from django.http import JsonResponse

from django.views.generic import ListView, DetailView

from cw.wordx import Crossword
from cw.forms import GenerateForm

class ListCross(ListView):
    model = CrossWord
    template_name = "cw_list.html"
    paginate_by = 12
class Play(DetailView):
    model = CrossWord
    template_name = "play.html"
files = ["json_data_1.json","json_data_2.json","json_data_3.json","json_data_4.json","json_data_5.json"]
def Load(request):
    # Ans.objects.all().delete()
    # return HttpResponse("deleted")

    for file in files:
        with open("cw//"+file,'r') as f:
            data = json.load(f)
            
            for key,value in data.items():
                clues = value.split('-_-')[0]
                length = len(key)
                popularity = len(clues)
                ans_qs = Ans.objects.filter(word=key)
                ans_exists = ans_qs.exists()
                if ans_exists:
                    ans_qs.update(popularity=F('popularity')+popularity)
                else:
                    Ans.objects.create(word=key,length=length,popularity=popularity,hint = clues)
                
                db.connections.close_all()
def Create(request):
    if request.method == 'POST':
        rows = int(request.POST.get('rows'))
        col = int(request.POST.get('col'))
        time = float (request.POST.get('time'))
        print(rows,col,time)
        available_words = Ans.objects.values_list('word','hint')
        available_words = list(available_words)
        print(type(available_words[0]))
        new_C = Crossword(rows,col,'$',available_words)
        ret = (new_C.compute_crossword(time))
        r = {'board':ret}
        return HttpResponse(json.dumps(r),content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
@require_POST
def Save(request):
    if request.method == 'POST':
        user = request.user
        b = request.POST.getlist('grid[]')
        print(b)
    
        scw = CrossWord.objects.create(board= b)
        a = []
        d = []
        w = []
        rows = len(b)
        col = len(b[0])
        for i,r in enumerate (b):
            for j,c in enumerate (r):
                if c!='$':
                    if j==0 and b[i][j+1]!='$':
                        w.append([i,j,'a'])
                    if j!=0 and b[i][j-1] =='$':
                        if j==col-1:
                            pass
                        elif b[i][j+1] !='$':
                            w.append([i,j,'a'])
                    if i == 0 and b [i+1][j]!= '$':
                        w.append([i,j,'d'])
                    elif i!=0  and b[i-1][j] =='$':
                        if i== rows-1:
                            continue
                        elif b[i+1][j] !='$':
                            w.append([i,j,'d'])
        for index,el in enumerate(w):
            i = el[0]
            j = el[1]
            if el[2]=='a':
                
                
                step = ''
                point = b[i][j]
                while b[i][j]!='$' :
                    
                    step += b[i][j]
                    j+=1
                    if j== col:
                        break
                w[index].append(step)
            else:
                step = ''
                while b[i][j]!='$':
                    step += b[i][j]
                    i+=1
                    if i== rows:
                        break
                w[index].append(step)
            hint = Ans.objects.filter(word=step)[0].hint
            Lead.objects.create( crosword = scw,user = user,i =el[0],j=el[1],orientation= el[2],word = step,hint = hint,pos = index)
        
        return HttpResponse(b)

def Main(request):
    context = {
        'form':GenerateForm
    }
    return render(request,'cw.html',context)

