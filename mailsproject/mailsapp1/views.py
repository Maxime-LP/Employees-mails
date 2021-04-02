from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    return HttpResponse("Page d'index")

def days(request,start,end,nb,threshold):
    return render(request, 'days.tmpl', 
        {
            'start':start,
            'end':end,
            'nb':nb,
            'threshold':threshold
        })