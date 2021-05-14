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
from app.models import User, mailAddress, Mail
from django.db.models import Count
from django.db.models.functions import TruncDate
from collections import defaultdict
from django.utils.timezone import datetime
import numpy as np

def index(request):
    
    context = {
        'segment':'index'
    }

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

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

    template = 'employees.html'

    start_date = request.GET.get('start_date')
    if not start_date:
        start_date = datetime(1900,1,1)

    end_date = request.GET.get('end_date')
    if not end_date:
        end_date=datetime(2100,1,1)
    
    threshold = request.GET.get('threshold')
    if not threshold:
        threshold = 0
    else:
        try:
            threshold = int(threshold)
        except ValueError:
            threshold = 0

    user = User.objects.all()

    lines = request.GET.get('lines')
    if not lines:
        paginator = Paginator(user, 10)
    else:
        try:
            paginator = Paginator(user, int(lines))
        except ValueError:
            paginator = Paginator(user, 10)

    page = request.GET.get('page')
    try:
        user = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user = paginator.page(paginator.num_pages)

    context = {
        "user":user,
        'start_date':start_date,
        'end_date':end_date,
        'threshold':threshold if threshold != 0 else ''
        }

    return render(request, template, context)

@login_required(login_url="/login/")
def couples(request):
    
    start_date = request.GET.get('start_date')
    if not start_date:
        start_date = 0
    else:
        print(start_date)

    end_date = request.GET.get('end_date')
    if not end_date:
        pass
    else:
        pass

    threshold = request.GET.get('threshold')
    if not threshold:
        threshold = 10
    else:
        threshold = int(threshold)

    lines = request.GET.get('lines')
    if not lines:
        lines = 10
    else:
        lines = int(lines)

    couples = User.objects.raw(f"""SELECT app_user.user1 as user1, app_user.user2 as user2, app_mail.mail, COUNT(app_mail.mail) as count FROM app_mail JOIN app_mailAddress
                                ON app_mailAddress.user_id = user1.id""")

    context = {
    
        }

    return render(request, 'couples.html', context)

@login_required(login_url="/login/")
def days(request):

    template = 'days.html'

    start_date = request.GET.get('start_date')
    if not start_date:
        start_date = datetime(1900,1,1)

    end_date = request.GET.get('end_date')
    if not end_date:
        end_date=datetime(2100,1,1)
    
    threshold = request.GET.get('threshold')
    if not threshold:
        threshold = 0
    else:
        try:
            threshold = int(threshold)
        except ValueError:
            threshold = 0

    mails_per_day = Mail.objects.annotate(time=TruncDate('date')).values('time')\
                    .filter(date__gte=start_date,date__lte=end_date).annotate(dcount=Count('enron_id')).order_by('-dcount').filter(dcount__gte=threshold)

    lines = request.GET.get('lines')
    if not lines:
        paginator = Paginator(mails_per_day, 10)
    else:
        try:
            paginator = Paginator(mails_per_day, int(lines))
        except ValueError:
            paginator = Paginator(mails_per_day, 10)

    page = request.GET.get('page')
    try:
        mails_per_day = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mails_per_day = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        mails_per_day = paginator.page(paginator.num_pages)

    context = {
        "days":mails_per_day,
        'start_date':start_date,
        'end_date':end_date,
        'threshold':threshold if threshold != 0 else ''
        }

    return render(request, template, context)

@login_required(login_url="/login/")
def profile(request):

    template = 'profile.html'

    name = request.GET.get('name')
    if not name:
        context = {'code':0}
        return render(request, template, context)
    else:
        try:
            user = User.objects.get(name=name)
        except:
            context = {'code':-1,
                        'name':name
                        }
            return render(request, template, context)
        
        emails = Mail.objects.raw(f"""SELECT m.* 
                                      FROM app_Mail AS m 
                                      JOIN app_mailAddress AS ma 
                                      ON ma.user_id = {user.id} 
                                      WHERE (ma.id = m.sender_id OR ma.id = m.recipient_id);""")
        average_response_time = 0
        number_of_responses = 0
        number_of_internal_mails = 0
        number_of_external_mails = 0
        response_time = 0
        internal_contacts = []
        daily_sent_mails = defaultdict(lambda: 0)
        daily_received_mails = defaultdict(lambda: 0)

        for m in emails:
            #2000-12-04 10:09:00+00:00
            try:           
                sender = User.objects.get(id=m.sender_id)
                recipient = User.objects.get(id=m.recipient_id)#m.recipient_id)
            except:
                print('mail_id:',m.enron_id, '- sender_id:', {m.sender_id}, '- recipient_id:', {m.recipient_id})
            if sender.name == user.name:
                daily_sent_mails[str(m.date)[:10]] += 1
                if recipient.inEnron:
                    number_of_internal_mails += 1
                    internal_contacts.append(recipient.name)
                else:
                    number_of_external_mails += 1

                if m.isReply:
                    try:
                        previous_mail = Mail.objects.raw(f"""SELECT mail
                                                             FROM app_Mail AS m 
                                                             WHERE m.sender_id = {m.recipient_id}
                                                                                AND m.recipient_id = {m.sender_id}
                                                                                AND m.date < {m.date} 
                                                             ORDER BY m.date DESC
                                                             LIMIT 1;""")
                    except django.core.exceptions.ObjectDoesNotExist:
                        previous_mail = None

                    if previous_mail is not None:
                        number_of_responses += 1
                        response_time += (m.date - previous_mail.date).total_seconds()

            else:
                daily_received_mails[str(m.date)[:10]]+=1
                if sender.inEnron:
                    number_of_internal_mails += 1
                else:
                    number_of_external_mails += 1
            
        if internal_contacts != []:
            internal_contacts = set(internal_contacts)
        else:
            internal_contacts = 0            
            
        if number_of_responses != 0:
            mean_response_time = response_time / number_of_responses
        
        if number_of_external_mails == 0:
            ratio = number_of_internal_mails
        else:
            ratio = number_of_internal_mails / number_of_external_mails
        

        context = {'code':1,
                   'name':name,
                   'category':user.category,
                   'average_sent':0,
                   'average_received':np.mean(list(daily_received_mails.values())),
                   'average_response_time':0,
                   'ie_ratio':0,
                   }

        return render(request, template, context)
    '''
    mails = Mail.objects.raw(f"""SELECT m.* FROM app_Mail AS m JOIN app_mailAddress AS ma ON ma.user_id = {user.id} WHERE (ma.id = m.sender_id OR ma.id = m.recipient_id);""")
    mean_response_time = 0
    number_of_responses = 0
    number_of_internal_mails = 0
    number_of_external_mails = 0
    internal_contacts = []
    daily_sent_mails = defaultdict(lambda: 0)
    daily_received_mails = defaultdict(lambda: 0)
    
    for m in mails:
        #2000-12-04 10:09:00+00:00
        sender=User.objects.get(id=m.sender_id)
        recipient=User.objects.get(id=m.recipient_id)

        if sender.name == user.name:
            daily_sent_mails[str(m.date)[:10]]+=1
            if recipient.inEnron:
                number_of_internal_mails+=1
                internal_contacts.append(recipient.name)
            else:
                number_of_external_mails+=1

            if m.isReply:
                try:
                    previous_mail = Mail.objects.raw(f"""SELECT mail FROM app_Mail WHERE mail.sender_id = {m.recipient_id} AND 
                                                        mail.recipient_id={m.sender_id} AND mail.date < {m.date} 
                                                        ORDER BY app_Mail.date DESC LIMIT 1;""")
                except django.core.exceptions.ObjectDoesNotExist:
                    previous_mail = None

                if previous_mail is not None:
                    number_of_responses+=1
                    mean_response_time += (m.date - previous_mail.date).total_seconds()

        else:
            daily_received_mails[str(m.date)[:10]]+=1
            if sender.inEnron:
                number_of_internal_mails+=1
            else:
                number_of_external_mails+=1
    if internal_contacts == []:
        internal_contacts = 0
    else:
        internal_contacts = set(internal_contacts)
        
    if number_of_responses!=0:
        mean_response_time /= number_of_responses
    
    if number_of_external_mails==0:
        ratio = number_of_internal_mails
    else:
        ratio = number_of_internal_mails/number_of_external_mails
    
    context = {
        'user':user,
        'daily_sent_mails_mean':np.mean(list(daily_sent_mails.values())),
        'daily_received_mails_mean':np.mean(list(daily_received_mails.values())),
        'mean_response_time': mean_response_time,
        'ratio':ratio,
        'internal_contacts':internal_contacts
        }

    return render(request, 'profile_enron.html', context)'''
