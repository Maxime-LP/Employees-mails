import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailsproject.settings')
import django
django.setup()
from django.utils.timezone import datetime, timedelta, make_aware, timezone
from mailsapp1.models import mailbox,mail_address,mail
import xml.etree.ElementTree as ET
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
def convert_date(input_date):
    #converts a naive datetime into an aware django datetime in UTC timezone
    #e.g. 4 Dec 2000 02:09:00 -0800 (PST) into 2000-12-04 10:09:00+00:00

    if input_date[1] == ' ': #ie if the day has only one digit (for string length consistency)
        input_date = '0'+input_date
    converted_date = datetime.strptime(input_date[:26], '%d %b %Y %H:%M:%S %z')

    #converting the date in UTC format
    UTC = timezone(timedelta(hours = 0))
    converted_date = converted_date.astimezone(UTC)

    return converted_date
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
            date_passed = False
            recipients_passed = False
            considering_a_forwarded_message = False

            #extraction des informations
            for line in file.readlines():
                if line[:6]=='Date: ' and not date_passed and not considering_a_forwarded_message:
                    date = convert_date(line[11:])
                    date_passed = True

                elif line[:6]=='From: ' and not sender_passed and not considering_a_forwarded_message:
                    sender = line[6:].replace(" ","")
                    sender_passed = True

                elif line[:4]=="To: " and not recipients_passed and not considering_a_forwarded_message:
                    recipients += re.split(',|, ',line[4:-1])
                    recipients_passed = True

                elif bool(re.match(r"-+ Forwarded by ",line)):
                    considering_a_forwarded_message = True

                elif considering_a_forwarded_message and bool(re.match(r".+<.+@.+>.+",line)):
                    previous_sender = re.search(r"<.+@.+>",line).group()[1:-1]
                    previous_date = re.search(r" on .*",line).group()[4:]


            #injection dans la db
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