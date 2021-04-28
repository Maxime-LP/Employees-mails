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
from django.utils.timezone import datetime, timezone
from app.models import Mailbox, mailAddress, Mail, User
import xml.etree.ElementTree as ET
from collections import defaultdict


## Preprocessing employes_enron.xml ##########################################

def preprocessXMLFile():
    path = os.getcwd()
    tree = ET.parse(path + '/employes_enron.xml')
    root = tree.getroot()

    for child in root:
        current_mailbox = Mailbox()
        current_user = User(inEnron = True)
        current_user.save()
        current_mailbox.save()
        
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
                new_mail = mailAddress(box_id = current_mailbox.id, address = subchild.attrib['address'], user_id = current_user.id)
                new_mail.save()
            
            elif subchild.tag == 'mailbox':
                current_mailbox.tag = subchild.text
        
        current_user.name = f"{first_name} {last_name}"
        current_mailbox.save()
        current_user.save()


## Usefull function ##########################################################

def convert_date(input_date):
    #converts a naive datetime into an aware django datetime in UTC timezone
    #e.g. 4 Dec 2000 02:09:00 -0800 (PST) into 2000-12-04 10:09:00+00:00

    if input_date[1] == ' ':            #ie if the day has only one digit
        input_date = '0'+input_date             #for string length consistency
    converted_date = datetime.strptime(input_date, '%d %b %Y %H:%M:%S %z')
    #converting the date in UTC format
    UTC = timezone(timedelta(hours = 0))
    converted_date = converted_date.astimezone(UTC)
    return converted_date

def get_most_recent_mail(list_of_mails):
    """
    Input must be a list of mail instances or an instance of mail
    """
    if isinstance(list_of_mails,Mail):
        return list_of_mails
    return max(list_of_mails, key=lambda x: x.date)

def PasDeDoublon(list: list ):
    new_list = []
    for element in list:
        if element not in new_list:
            new_list.append(element)
    return new_list

def progress_info(n, prefix="Computing:", size=40, file=sys.stdout):
    if n%100 == 0:
        print("{} {:2.1%}".format(prefix, n/517401), end="\r")
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
            with open(fp, 'r') as f:
                try:
                    e = email.message_from_file(f)
                except UnicodeDecodeError as error:
                    # use 'iso-8859-1' charset
                    pass

                mail_id = e.get('Message-ID')
                emails[mail_id] = {key:value for key, value in e.items()}
                emails[mail_id]['fp'] = fp


    print(f'Completed: {n} files have been read in {round(time()-t0,2)}s.')

    print('Create pickle: ...', end="\r")
    with open(os.path.join(name), "wb") as data:
        pickle.dump(emails, data)
    print(f'Create pickle: succeeds. {len(emails)} emails have been read.')

    return os.path.join(name)


def load_data(pickle_fp):
    print('Load data: ...', end='\r')
    with open(pickle_fp, "rb") as data:
        emails = pickle.load(data)
    print(f'Load data: succeeds. {len(emails)} emails have been loaded.')
    return emails


def catch_infos(mail):

    # mail_id
    mail_id = mail['Message-ID']
    
    # mail_date
    try:
        mail_date = convert_date(mail['Date'][5:-6])
    except:
        # there is only one email that throws an exception.
        # --> /home/amait/Downloads/maildir/lokey-t/calendar/33.
        mail_date = None
    
    # mail_subject
    mail_subject = mail['Subject']
    
    # mail_sender
    mail_sender = mail['From']

    # mail_recipients
    mail_recipients = []
    recipient_fields = ['To', 'X-To', 'Cc', 'X-cc', 'Bcc', 'X-bcc']
    for field in recipient_fields:
        try:
            mail_recipients += re.split(',', re.sub(r"\s+", "", mail[field])) #flags=re.UNICODE))
        except KeyError: pass
    # remove recipients without '@'
    regex = re.compile(r'.*@.*')
    mail_recipients = [elm for elm in mail_recipients if regex.match(elm)]
    # remove duplicate recipients
    mail_recipients = list(set(mail_recipients))

    infos = [mail_id, mail_date, mail_subject, mail_sender, mail_recipients]
    
    return infos


def update_db(infos):
    mail_id, mail_date, mail_subject, mail_sender, mail_recipients = infos
    pass
    '''
    print(type(mail_id))
    print(mail_id)
    print(mail_sender)
    input('pass')
    # save mail
    regex = re.compile(r'Re:')
    mail_isReply = bool(regex.match(mail_subject))
    mail = Mail(enron_id = mail_id,
                date = mail_date,
                subject = mail_subject,
                sender = mail_sender,
                recipient = mail_recipients,
                isReply = mail_isReply
                )
    #mail.save()
    '''

def update_database(emails):
    n = 1
    for mail in emails.values():
        infos = catch_infos(mail)
        update_db(infos)
        n = progress_info(n, prefix='Updating database:')
    print('Update database: succeeds.')


if __name__=="__main__":

    x = input('Proprocess XML file (0/1)? ')
    if bool(int(x)):
        preprocessXMLFile()
    
    data_fp = '/home/amait/Downloads/maildir'
    pkl_file_name = 'headers.pkl'

    x =  input('Create pickle file (0/1)? ')
    if bool(int(x)):
        pkl_fp = create_pickle(data_fp, name=pkl_file_name)
    else:
        pkl_fp = os.path.join(pkl_file_name)

    emails = load_data(pickle_fp=pkl_fp)

    update_database(emails)
    
