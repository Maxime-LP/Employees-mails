# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import django
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from app.models import User, Mailbox, mailAddress, Mail

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
        usr = User.objects.all()
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
        usr = User.objects.raw(f'SELECT u.id, u.name FROM app_user AS u LIMIT {lines}')
    else:
        usr = User.objects.raw(f'SELECT u.id, u.name FROM app_user AS u LIMIT {lines}')

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

@login_required(login_url="/login/")
def couples(request):
    pass

@login_required(login_url="/login/")
def days(request):
    pass

@login_required(login_url="/login/")
def profile(request):

    user = request.GET.get('user')
    if not user:
        raise Exception("Please enter a name")
    try:
        user = User.objects.get(name = user)
    except django.core.exceptions.ObjectDoesNotExist:
        raise Exception("User does not exist")

    sent_mails = Mail.objects.raw('SELECT mail FROM Mail JOIN mailAddress ON mailAdress.user_id = user.id AND mailAdress.id = mail.sender_id;')
    mean_response_time = 0
    n=0

    for current_mail in sent_mails:
        if current_mail.reponse:
            try:
                previous_mail = Mail.objects.raw("""SELECT mail FROM Mail WHERE current_mail.sender_id == mail.recipient_id, mail.date < current_mail.date 
                                                    ORDER BY Mail.date DESC LIMIT 1;""")
            except django.core.exceptions.ObjectDoesNotExist:
                previous_mail = None

            if previous_mail is not None:
                n+=1
                mean_response_time += current_mail.date - previous_mail.date #??
    
    if n!=0:
        mean_response_time /= n

    number_of_internal_mails = Mail.objects.raw("""SELECT mail COUNT(*) FROM Mail JOIN app_user 
                                                ON app_user.inEnron=1, 
                                                                                                        """)
    number_of_external_mails = 0

    internal_contacts = User.objects.raw()

    context = {
        'user':user,
        'mean_response_time': mean_response_time
        }

    return render(request, 'profile_enron.html', context)