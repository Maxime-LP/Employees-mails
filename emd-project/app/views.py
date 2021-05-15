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
from django.db.models.functions import TruncMonth, ExtractMonth
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate
from collections import defaultdict
from django.utils.timezone import datetime
from numpy import mean

@login_required(login_url="/login/")
def index(request):

    template = 'index.html'

    email_exchanges = Mail.objects.count()
    num_collaborators = User.objects.filter(in_enron=True).count()
    extern_contact = User.objects.filter(in_enron=False).count()
    intern_exchange = Mail.objects.filter(is_intern=True).count() / Mail.objects.filter(is_intern=False).count()

    context = {'email_exchanges':email_exchanges,
               'num_collaborators':num_collaborators,
               'extern_contact':extern_contact,
               'intern_exchange':round(intern_exchange,1),}

    return render(request, template, context)

@login_required(login_url="/login/")
def employees(request):

    template = 'employees.html'

    start_date = request.GET.get('start_date')
    if not start_date:
        start_date = '1900-01-01'

    end_date = request.GET.get('end_date')
    if not end_date:
        end_date='2100-01-01'
    
    low_thr = request.GET.get('low_thr')
    if not low_thr:
        low_thr = 0
    else:
        try:
            low_thr = int(low_thr)
        except ValueError:
            low_thr = 0

    high_thr = request.GET.get('high_thr')
    if not high_thr:
        high_thr = 10**6
    else:
        try:
            high_thr = int(high_thr)
        except ValueError:
            high_thr = 10**6

    user = User.objects.all()[:3]
    '''mci = User.objects.raw(f"""select u.name, u.category, cnt.c
                                        from app_user as u, (select sender_id, count(sender_id) as c 
                                                             from app_mail 
                                                             where is_intern=True and date(date) > {start_date} AND date(date) < {end_date} 
                                                             group by sender_id) as cnt 
                                        where cnt.sender_id = u.id and cnt.c > {low_thr} and cnt.c < {high_thr} 
                                        ORDER BY c DESC;""")'''
    mci = User.objects.raw(f"""select u.id, u.name, u.category, cnt.c
                            from app_user as u, (select sender_id, count(sender_id) as c 
                                                 from app_mail 
                                                 where is_intern=True and date(date) > '{start_date}' and date(date) < '{end_date}'
                                                 group by sender_id) as cnt 
                            where cnt.sender_id = u.id and cnt.c > '{low_thr}' and cnt.c < '{high_thr}' 
                            ORDER BY c DESC;""")


    tqr = 0
    gib = 0

    lines = request.GET.get('lines')
    if not lines:
        paginator = Paginator(mci, 5)
    else:
        try:
            paginator = Paginator(mci, int(lines))
        except ValueError:
            paginator = Paginator(mci, 5)

    page = request.GET.get('page')
    try:
        mci = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, delivers first page.
        mci = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), delivers last page of results.
        mci = paginator.page(paginator.num_pages)

    context = {
        "user":user,
        'mci':mci,
        'tqr':tqr,
        'gib':gib,
        'start_date':start_date,
        'end_date':end_date,
        'low_thr':low_thr if low_thr != 0 else '',
        'high_thr':high_thr if high_thr != 10**6 else ''
        }

    return render(request, template, context)

@login_required(login_url="/login/")
def couples(request):
    
    template = 'couples.html'

    start_date = request.GET.get('start_date')
    if not start_date:
        start_date = datetime(1900,1,1)

    end_date = request.GET.get('end_date')
    if not end_date:
        end_date = datetime(2100,1,1)
    
    low_thr = request.GET.get('low_thr')
    if not low_thr:
        low_thr = 0
    else:
        try:
            low_thr = int(low_thr)
        except ValueError:
            low_thr = 0

    high_thr = request.GET.get('high_thr')
    if not high_thr:
        high_thr = 10**6
    else:
        try:
            high_thr = int(high_thr)
        except ValueError:
            high_thr = 10**6

    user = User.objects.all()[:3]
    couples = 0
    '''
    couples = User.objects.raw(f"""SELECT app_user.user1 as user1, app_user.user2 as user2, app_mail.mail, COUNT(app_mail.mail) as count FROM app_mail JOIN app_mailAddress
                                ON app_mailAddress.user_id = user1.id""")

    lines = request.GET.get('lines')
    if not lines:
        paginator = Paginator(couples, 5)
    else:
        try:
            paginator = Paginator(couples, int(lines))
        except ValueError:
            paginator = Paginator(couples, 5)

    page = request.GET.get('page')
    try:
        couples = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        couples = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        couples = paginator.page(paginator.num_pages)
    '''
    context = {
        "user":user,
        'couples':couples,
        'start_date':start_date,
        'end_date':end_date,
        'low_thr':low_thr if low_thr != 0 else '',
        'high_thr':high_thr if high_thr != 10**6 else ''
        }

    return render(request, template, context)

@login_required(login_url="/login/")
def days(request):

    template = 'days.html'

    start_date = request.GET.get('start_date')
    if not start_date:
        start_date = datetime(1900,1,1)

    end_date = request.GET.get('end_date')
    if not end_date:
        end_date = datetime(2100,1,1)
    
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
def profileold(request):

    template = 'profile.html'

    name = request.GET.get('name')
    if not name:
        context = {'code':0}
        return render(request, template, context)
    
    try:
        user = User.objects.get(name=name)
    except:
        context = {'code':-1,
                    'name':name
                    }
        return render(request, template, context)

    if user.in_enron == False:
        context = {'code':-2,
                    'name':name
                    }
        return render(request, template, context)
    
    #sent_per_day = Mail.objects.filter(f"""select avg(cnt.c) from (select date(date), count(date) as c from app_mail where sender_id=63 group by date(date)) as cnt;""")
    #sent_per_day  = Mail.objects.annotate(time=TruncDate('date')).values('time').filter(sender_id=user.id).annotate(dcount=Count('enron_id')).order_by('-dcount')
    #print(sent_per_day)
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
        
        sender = User.objects.get(id=m.sender_id)
        recipient = User.objects.get(id=m.recipient_id)
        
        print(sender.name)
        if sender.name == user.name:
            print('ok')
            daily_sent_mails[str(m.date)[:10]] += 1
            if recipient.in_enron:
                number_of_internal_mails += 1
                internal_contacts.append(recipient.name)
            else:
                number_of_external_mails += 1

            if m.is_reply:
                print('in reply')
                try:
                    previous_mail = Mail.objects.raw(f"""SELECT mail FROM app_mail AS m WHERE m.sender_id = {m.recipient_id} AND m.recipient_id = {m.sender_id} AND m.date < {m.date} ORDER BY m.date DESC LIMIT 1;""")
                except django.core.exceptions.ObjectDoesNotExist:
                    previous_mail = None

                if previous_mail is not None:
                    number_of_responses += 1
                    response_time += (m.date - previous_mail.date).total_seconds()

        else:
            daily_received_mails[str(m.date)[:10]]+=1
            if sender.in_enron:
                number_of_internal_mails += 1
            else:
                number_of_external_mails += 1
        
    if internal_contacts != []:
        internal_contacts = set(internal_contacts)
    else:
        internal_contacts = 0            
        
    if number_of_responses != 0:
        print('ok')
        print(response_time,'/', number_of_responses,"=", average_response_time)
        average_response_time = response_time / number_of_responses
    
    if number_of_external_mails == 0:
        ie_ratio = number_of_internal_mails
    else:
        ie_ratio = number_of_internal_mails / (number_of_internal_mails + number_of_external_mails)
    
    print(list(daily_sent_mails.values()))
    context = {'code':1,
               'name':name,
               'category':user.category,
               'average_sent':round(mean(list(daily_sent_mails.values())),2),
               'average_received':round(mean(list(daily_received_mails.values())),2),
               'average_response_time':average_response_time,
               'number_of_internal_mails':number_of_internal_mails,
               'number_of_external_mails':number_of_external_mails,
               'internal_contacts':internal_contacts,
               }

    return render(request, template, context)


def profile(request):

    template = 'profile.html'

    name = request.GET.get('name')
    if not name:
        context = {'code':0}
        return render(request, template, context)
    
    try:
        user = User.objects.get(name=name)
    except:
        context = {'code':-1,
                    'name':name
                    }
        return render(request, template, context)

    if user.in_enron == False:
        context = {'code':-2,
                    'name':name
                    }
        return render(request, template, context)
    
    
    #mails sent / received per day
    user_mails = mailAddress.objects.filter(user_id=user.id)
    
    sent_per_day = Mail.objects.filter(sender_id__in=user_mails).annotate(time=TruncDate('date'))\
                .values('time').annotate(dcount=Count('enron_id')).aggregate(Avg('dcount'))

    
    
    received_per_day = Mail.objects.filter(recipient_id__in=user_mails).annotate(time=TruncDate('date'))\
                .values('time').annotate(dcount=Count('enron_id')).aggregate(Avg('dcount'))

    
    

    #SELECT mail FROM app_mail WHERE mail.sender_id = m.recipient_id AND mail.recipient_id = m.sender_id AND mail.date < m.date ORDER BY mail.date DESC LIMIT 1
    #average response time
    average_response_time = 0

    #I/E Ratio

    number_of_internal_mails = 0
    number_of_external_mails = 0

    #Internal contacts

    internal_contacts = 0

    context = {'code':1,
               'name':name,
               'category':user.category,
               'average_sent':sent_per_day,
               'average_received':received_per_day,
               'average_response_time':average_response_time,
               'number_of_internal_mails':number_of_internal_mails,
               'number_of_external_mails':number_of_external_mails,
               'internal_contacts':internal_contacts,
               }

    return render(request, template, context)