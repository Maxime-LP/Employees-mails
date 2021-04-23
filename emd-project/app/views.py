# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from app.models import user, mailbox, mail_address, mail

#@login_required(login_url="/login/")
def index(request):
    
    context = {
        'segment':'index'
    }

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def employees(request):

    quer = request.GET.get('quer')
    #current_name = query
    if not quer:
        usr = user.objects.all()
        pass
    else:
        pass

    start_date = request.GET.get('start_date')
    if not start_date:
        print(type(start_date))
    else:
        print(start_date)

    end_date = request.GET.get('end_date')
    if not end_date:
        pass
    else:
        pass

    lines = request.GET.get('lines')
    if not lines:
        lines = 10
        usr = user.objects.raw(f'SELECT u.id, u.name FROM app_user AS u LIMIT {lines}')
    else:
        usr = user.objects.raw(f'SELECT u.id, u.name FROM app_user AS u LIMIT {lines}')

    paginator = Paginator(usr, 300)
    page = request.GET.get('page')
    try:
        usr = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        usr = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        usr = paginator.page(paginator.num_pages)
    context = {
        'user':usr,
        'current_name':quer,
        'start_date':start_date,
        'end_date':end_date,
        'lines':lines,


        }

    load_template = request.path.split('/')[-1]
    template = loader.get_template('employees.html')

    return render(request, 'employees.html', context)

    """
    return render(request, 'employees.html', 
        {
        'user':user.objects.raw(
            #'SELECT u.name, u.category, ma.user FROM app_user AS u, app_mail_address AS ma WHERE u.name==ma.user'
            'SELECT u.id, u.name FROM app_user AS u LIMIT 5'
            )
        })
    """
