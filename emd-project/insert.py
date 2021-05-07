#!/usr/bin/env python3
import os
import sys
import pickle
import re
import email
from time import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from django.utils.timezone import datetime, timezone, timedelta
from app.models import mailAddress, Mail, User
import xml.etree.ElementTree as ET
from collections import defaultdict
from multiprocessing import Pool
from tqdm import tqdm


## Preprocessing employes_enron.xml ##########################################

def preprocessXMLFile():
    path = os.getcwd()
    tree = ET.parse(path + '/employes_enron.xml')
    root = tree.getroot()

    for child in root:
        current_user = User(inEnron = True)
        current_user.save()
        
        last_name = ''
        first_name = ''

        try:
            current_user.category = child.attrib['category']
        except KeyError:
            current_user.category = 'Employee'

        for subchild in child:
            if subchild.tag == 'lastname':
                last_name = subchild.text

            elif subchild.tag == 'firstname':
                first_name = subchild.text

            elif subchild.tag == 'email':
                new_mail = mailAddress(address = subchild.attrib['address'], user = current_user)
                new_mail.save()
        
        current_user.name = f"{first_name} {last_name}"
        current_user.save()


## Usefull function ##########################################################

def convert(date):
    #converts a naive datetime into an aware django datetime in UTC timezone
    #e.g. 4 Dec 2000 02:09:00 -0800 (PST) into 2000-12-04 10:09:00+00:00
    if date[1] == ' ':            #ie if the day has only one digit
        date = '0' + date             #for string length consistency
    converted_date = datetime.strptime(date, '%d %b %Y %H:%M:%S %z')
    #converting the date in UTC format
    UTC = timezone(timedelta(hours = 0))
    converted_date = converted_date.astimezone(UTC)
    return converted_date

def get_name(mail_address):
    
    mail_address = re.sub(r'[\'\"]', "", mail_address)

    regex1 = re.compile(r'([a-zA-Z]*[\._-][a-zA-Z]*)@.*\..{,3}')
    found = regex1.search(mail_address)
    if found:
        return str.title(re.sub(r'[\._-]', ' ',found.group(1))).strip()
    
    regex2 = re.compile(r'^<?(.*)@.*>$')
    found = regex2.search(mail_address)
    if found:
        return str.title(found.group(1)).strip()
    
    regex3 = re.compile(r'^([A-Za-z]*)@')
    found = regex3.search(mail_address)
    if found:
        return re.sub(r"([A-Z])", r" \1", found.group(1)).strip()

    return mail_address

def inEnron(mail_address):
    regex = re.compile(r'.*@enron\..*', re.IGNORECASE)
    found = regex.search(mail_address)
    return False if found==None else True

def isReply(mail_subject):
    regex = re.compile(r'^[Rr][Ee]:')
    found = regex.search(mail_subject)
    return False if found==None else True

def progress_info(n, prefix="Computing:", size=40, file=sys.stdout):
    if n%10 == 0:
        print("{} {} / {:2.1%}".format(prefix, n, n/517401), end="\r")
    return n + 1

##############################################################################

## Create pickle #############################################################

def create_pickle(data_fp, name):
    n = 0
    emails = {}
    t0 = time()
    for root, dirs, files in os.walk(data_fp, topdown=False):
        for file in files:
            fp = os.path.join(root, file)
            n  = progress_info(n, prefix="Analyzing data:")
            
            with open(fp, 'r', encoding='utf-8') as f:
                try:
                    e = email.message_from_file(f)
                except UnicodeDecodeError as error:
                    with open(fp, 'r', encoding='iso-8859-1') as f:
                        try:
                            e = email.message_from_file(f)
                        except UnicodeDecodeError as error:
                            print('UnicodeDecodeError:', fp)

            mail_id = e.get('Message-ID')
            emails[mail_id] = {key:value for key, value in e.items()}
            emails[mail_id]['fp'] = fp



    print(f'Completed: {n} files have been read in {round(time()-t0,2)}s.')

    print('Create pickle: ...', end="\r")
    with open(os.path.join(name), "wb") as data:
        pickle.dump(emails, data)
    print(f'Create pickle: succeeds. {len(emails)} emails have been save.')

    return os.path.join(name)


def load_data(pickle_fp):
    print('Load data: ...', end='\r')
    with open(pickle_fp, "rb") as data:
        emails = pickle.load(data)
    print(f'Load data: succeeds. {len(emails)} emails have been loaded.')
    return emails


def catch_infos(email):

    # mail_id
    email_id = email['Message-ID']
    
    # mail_date
    try:

        email_date = convert(email['Date'][5:-6])

    except KeyError:
        # there is only one email that throws an exception.
        # --> /home/amait/Downloads/maildir/lokey-t/calendar/33.
        email_date = None
    
    # mail_subject
    email_subject = email['Subject']
    
    # mail_sender
    email_sender = email['From']

    # mail_recipients
    email_recipients = []
    recipient_fields = ['To', 'X-To', 'Cc', 'X-cc', 'Bcc', 'X-bcc']
    for field in recipient_fields:
        try:
            email_recipients += re.split(',', re.sub(r"\s+", "", email[field])) #flags=re.UNICODE))
        except KeyError: pass
    # remove recipients without '@'
    regex = re.compile(r'.*@.*')
    email_recipients = [elm for elm in email_recipients if regex.match(elm)]
    # remove duplicate recipients
    email_recipients = list(set(email_recipients))

    infos = [email_id, email_date, email_subject, email_sender, email_recipients]
    
    return infos


def update_db(infos):
    
    mail_id, mail_date, mail_subject, sender_address, recipients_address = infos
    
    try:
        sender_address_ = mailAddress.objects.get(address=sender_address)
    except django.core.exceptions.ObjectDoesNotExist:
        try:
            sender_ = User.objects.get(name=get_name(sender_address))
        except:
            sender_ = User(name=get_name(sender_address),
                          inEnron=inEnron(sender_address),
                          category='Unknown')
            sender_.save()
        sender_address_ = mailAddress(address=sender_address, user=sender_)
        try:
            sender_address_.save()
        except django.db.utils.DataError:
            print(mail_id, ':', sender_address)

    for recipient_address in recipients_address:
        try:
            recipient_address_ = mailAddress.objects.get(address=recipient_address)
        except django.core.exceptions.ObjectDoesNotExist:
            try:
                recipient_address_ = User.objects.get(name=get_name(recipient_address))
                recipient_ = recipient_address_.user
            except:
                recipient_ = User(name=get_name(recipient_address),
                              inEnron=inEnron(recipient_address),
                              category='Unknown')
                try:
                    recipient_.save()
                except django.db.utils.DataError:
                    print(mail_id, ':', recipient_address)

            recipient_address_ = mailAddress(address=recipient_address, user=recipient_)
            recipient_address_.save()
        
        mail_ = Mail(enron_id=mail_id,
                    date=mail_date,
                    subject=mail_subject,
                    sender=sender_address_,
                    recipient=recipient_address_,
                    isReply=isReply(mail_subject))
        try:
            mail_.save()
        except django.db.utils.DataError:
            print(mail_id)

'''
def update(email):
    try:
        email_id = email['Message-ID']
        mail = Mail.objects.get(enron_id=email_id)
    except django.core.exceptions.ObjectDoesNotExist:
        infos = catch_infos(email)
        update_db(infos)
'''

if __name__=="__main__":

    data_fp = '/home/amait/Downloads/maildir'
    pkl_file_name = 'headers.pkl'
    
    x = input('Preprocess XML file (0/1)? ')
    if x == '1':
        preprocessXMLFile()
    
    x = input('Create pickle file (0/1)? ')
    if x == '1':
        pkl_fp = create_pickle(data_fp, name=pkl_file_name)
    else:
        pkl_fp = os.path.join(pkl_file_name)

    x = input('Update database (0/1)? ')
    if x == '1':
        emails = load_data(pickle_fp=pkl_fp)
        '''
        with Pool(processes=os.cpu_count()) as p:
            res = list(tqdm(p.imap(update, emails.values()), total=len(emails), leave=False))
        '''
        n = 1
        for email in emails.values():
            try:
                email_id = email['Message-ID']
                mail = Mail.objects.get(enron_id=email_id)
            except django.core.exceptions.ObjectDoesNotExist:
                infos = catch_infos(email)
                update_db(infos)
            n = progress_info(n, prefix='Updating database:')
        
        print('Update database: succeeds.')
