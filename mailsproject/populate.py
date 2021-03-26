import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailsproject.settings')
import django
django.setup()

from django.utils.timezone import make_aware, datetime, get_current_timezone, tzinfo
import pytz
from mailsapp1.models import mailbox,mail_address,mail
import xml.etree.ElementTree as ET
import zipfile
import re

############################
path = r'C:\Users\lepau\OneDrive\Desktop'
###Populating mailbox and mail_address databases
#uncomment to populate
"""
#xml file
tree = ET.parse(path + '\employes_enron.xml')
root = tree.getroot()

for child in root:
    current_mailbox = mailbox()
    current_mailbox.save()

    try:
        current_mailbox.category = child.attrib['category']
    except KeyError:
        current_mailbox.category = 'Employee'

    for subchild in child:
        if subchild.tag == 'lastname':
            current_mailbox.last_name = subchild.text

        elif subchild.tag == 'firstname':
            current_mailbox.first_name = subchild.text

        elif subchild.tag == 'email':
            new_mail = mail_address()
            new_mail.box_id = current_mailbox.id
            new_mail.address = subchild.attrib['address']
            new_mail.save()
        
        elif subchild.tag == 'mailbox':
            current_mailbox.tag = subchild.text

    current_mailbox.save()
"""

############################
def convert_date(date):
    #converts a naive datetime into an aware django datetime
    #e.g. Mon, 4 Dec 2000 02:09:00 -0800 (PST) into 2000-12-04 02:09:00 PST

    if date[1] == ' ': #ie if the day has only one digit
        date = '0'+date
    months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    timezone = date[28:31] #PDT : UTC - 7 (summer time DST), PST : UTC - 8
    print(timezone)
    datet = datetime(
        year = int(date[7:11]), month = int(months[date[3:6]]), day = int(date[:2]),
        hour = int(date[12:14]), minute = int(date[15:17]), second = int(date[18:20])
    )
    date = make_aware(datet, is_dst=(timezone=='PST'))
    print(date)
    date = make_aware(datet, is_dst=(timezone=='PDT'))
    print(date)
    return date
############################


data = path + r"\mailbox"

for folder,sub_folder,files in os.walk(data):
    for file in files:
        file_path = os.path.join(folder,file)
        print("\n fp : ",file_path)
        
        #lecture d'un mail
        with open(file_path,'r') as file:
            recipients = []
            sender_passed = False
            considering_a_forwarded_message = False

            #extraction des informations
            for line in file.readlines():
                if line[:6]=='Date: ' and not considering_a_forwarded_message:
                    date = convert_date(line[11:])

                elif line[:6]=='From: ' and not sender_passed and not considering_a_forwarded_message:
                    sender = line[6:].replace(" ","")
                    sender_passed = True

                elif line[:4]=="To: " and not considering_a_forwarded_message:
                    recipients += re.split(',|, ',line[4:-1])

                elif bool(re.match(r"-+ Forwarded by ",line)):
                    considering_a_forwarded_message = True

                elif considering_a_forwarded_message and bool(re.match(r".+<.+@.+>.+",line)):
                    previous_sender = re.search(r"<.+@.+>",line).group()[1:-1]
                    previous_date = re.search(r" on .*",line).group()[4:]


            #injection dans la db
                #
                #
                #
            mailbox_tag = re.search(r"\w+-\w",folder).group()
            current_mailbox = mailbox.objects.get(tag=mailbox_tag)

            try:
                sender_id = mail_address.objects.get(address=sender).id
            except django.core.exceptions.ObjectDoesNotExist:
                #le mail provient d'une adresse exterieure
                sender_id = None
            
            for recipient in recipients:
                new_mail = mail()
                new_mail.mail_date = date
                
                try:
                    recipient_id = mail_address.objects.get(address=recipient).id
                except django.core.exceptions.ObjectDoesNotExist:
                    #le mail va vers une adresse exterieure
                    recipient_id = None

                new_mail.recipient_mail_id = recipient_id
                new_mail.sender_mail_id = sender_id

                new_mail.previous_mail_id = None
                new_mail.response_mail_id = None
                new_mail.save()

            #il faudra ensuite regarder s'il existe dans la db un mail avec sender = previous_sender et date = previous_date pour raccorder les deux mails, sinon on le créera