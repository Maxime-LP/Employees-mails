#!/usr/bin/env python3
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from django.utils.timezone import datetime, timedelta, make_aware, timezone
from app.models import mailbox, mail_address, mail, user
import xml.etree.ElementTree as ET
import re

##################################################

path = os.getcwd()
#path = r'/home/amait/Documents/enron-mails/'
#path = r'C:\Users\lepau\OneDrive\Desktop'

###Populate mailbox and mail_address databases
#uncomment to populate
'''
#xml file
tree = ET.parse(path + '/employes_enron.xml')
root = tree.getroot()

for child in root:
    current_mailbox = mailbox()
    current_user = user()
    current_user.inEnron = True
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
            new_mail = mail_address()
            new_mail.box_id = current_mailbox.id
            new_mail.address = subchild.attrib['address']
            new_mail.user_id = current_user.id
            new_mail.save()
        
        elif subchild.tag == 'mailbox':
            current_mailbox.tag = subchild.text
    
    current_user.name = f"{first_name} {last_name}"
    current_mailbox.save()
    current_user.save()
'''
##################################################

############################
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
    if isinstance(list_of_mails,mail):
        return list_of_mails
    return max(list_of_mails, key=lambda x: x.date)

def PasDeDoublon(list: list ):
    new_list = []
    for element in list:
        if element not in new_list:
            new_list.append(element)
    return new_list

############################

#data =  "/home/amait/Downloads/maildir"
data = '/home/amait/Downloads/maildir'

#Populate mail database
for folder,sub_folder,files in os.walk(data):

    for file in files:
        file_path = os.path.join(folder,file)
        print("\n fp : ",file_path)
        
        #lecture d'un mail
        with open(file_path,'r') as file:
            recipients = []
            recipients_names = []
            header = True
            response = False

            ###### extraction des informations ######
            lines = iter(file.readlines())
            for line in lines:
                if header:
                    if (line[:4]=="To: " or line[:4]=="Cc: ") and len(line) > 4:
                        recipients += re.split(', |,',line[4:-1])
                        line = next(lines)

                        while bool(re.match(r"^[ \t]+.*$",line)):
                            recipients += re.split(', |,',line[1:-1])
                            line = next(lines)
                        recipients = [rec for rec in recipients if rec!=""]
                    
                    if line[:5]=="Bcc: " and len(line) > 5:
                        recipients += re.split(', |,',line[5:-1])
                        line = next(lines)

                        while bool(re.match(r"^[ \t]+.*$",line)):
                            recipients += re.split(', |,',line[1:-1])
                            line = next(lines)
                        recipients = [rec for rec in recipients if rec!=""]
                    
                    if line[:6]=='From: ':
                        sender_mail = line[6:-1]

                    elif line[:6]=='Date: ':
                        date = convert_date(line[11:-7])

                    elif line[:9] == "Subject: ":
                        subject = line[9:]
                        
                        if subject[:3] == "Re:":
                            response = True

                    elif line[:8]=="X-From: ":
                        line = line[8:]

                        if bool(re.match(r'^".+" <.+@.+>.*$', line)):
                            infos = re.split('"',line)
                            #['',name,mail]
                            sender_name = infos[1]

                        elif bool(re.match(r'.+@.+$', line)):
                            sender_name = None
                        
                        elif bool(re.match(r'^[^@.]+$',line)):
                            sender_name = line[:-1]
                    
                    if line[:6]=="X-To: " and len(line)>6:
                        if not bool(re.match(r"^X-To: undisclosed-recipients:, *$",line)):
                            if bool( re.match(r"^X-To: ([^@\.\t\n]+,?)+( )*$", line) ):
                                recipients_names += re.split(', ',line[6:-1])
                                line = next(lines)

                                while bool(re.match(r"^[ \t]+.*$",line)):
                                    recipients_names += re.split(', |,',line[1:-1])
                                    line = next(lines)
                                recipients_names = [rec for rec in recipients_names if rec!=""]

                    if line[:6]=="X-cc: " and len(line) > 6:
                        if bool( re.match(r"^X-cc: ([^@\.\t\n]+,?)+ *$", line) ):
                            recipients_names += re.split(', ',line[6:-1])
                            line = next(lines)

                            while bool(re.match(r"^[ \t]+.*$",line)):
                                recipients_names += re.split(', |,',line[1:-1])
                                line = next(lines)
                            recipients_names = [rec for rec in recipients_names if rec!=""]

                    if line[:7]=="X-bcc: ":
                        header = False
                        
                        if len(line) > 7:
                            if bool( re.match(r"^X-bcc: ([^@\.\t\n]+,?)+ *$", line) ):
                                recipients_names += re.split(', ',line[7:-1])
                                line = next(lines)

                                while bool(re.match(r"^[ \t]+.*$",line)):
                                    recipients_names += re.split(', |,',line[1:-1])
                                    line = next(lines)
                                recipients_names = [rec for rec in recipients_names if rec!=""]


            recipients = PasDeDoublon(recipients)
            recipients_names = PasDeDoublon(recipients_names)

            ###### injection dans la db ######
            mailbox_tag = re.findall(r"\w+-\w",folder)
            #pour eviter les bugs avec des noms de dossier correspondant au pattern
            for tag in mailbox_tag:
                try:
                    current_mailbox = mailbox.objects.get(tag=tag)
                except django.core.exceptions.ObjectDoesNotExist:
                    pass
            
            #### Recupération des instances correspondant au profil utilisateur et au mail de l'envoyeur ####
            try:
                sender_mail = mail_address.objects.get(address=sender_mail)  #on récupère le mail de l'envoyeur
            except django.core.exceptions.ObjectDoesNotExist:                   #s'il n'existe pas dans la db, on le crée

                if sender_name is not None: 
                    try:
                        sender = user.objects.get(name=sender_name)
                    except django.core.exceptions.ObjectDoesNotExist:
                        sender = user(name = sender_name)
                else: 
                    sender = user(name = sender_name)

                if bool(re.match(r'^.+@.*enron.com$',sender_mail)):
                    sender.inEnron = True
                else:
                    sender.inEnron = False

                sender.save()
                sender_mail = mail_address(address = sender_mail, user_id = sender.id)
                sender_mail.save()

            try:
                sender = user.objects.get(pk=sender_mail.user_id)   #on récupère le profil de l'envoyeur
            except django.core.exceptions.ObjectDoesNotExist:             #s'il n'existe pas dans la db, on le crée

                if sender_name is not None: 
                    try:
                        sender = user.objects.get(name=sender_name)
                    except django.core.exceptions.ObjectDoesNotExist:
                        sender = user(name = sender_name)
                else: 
                    sender = user(name = sender_name)
                
                if bool(re.match(r'^.+@.*enron.com$',sender_mail.address)):
                    sender.inEnron = True
                else:
                    sender.inEnron = False
                
                sender.save()

            #### Parcours de la liste des destinataires ####
            for index,recipient in enumerate(recipients):

                try:
                    recipient_mail = mail_address.objects.get(address=recipient)    #on récupère l'id de l'envoyeur   
                    recipient = recipient_mail.user
                except django.core.exceptions.ObjectDoesNotExist:
                    #si le destinataire utilise une adresse enron on lui crée un enregistrement
                    if bool(re.match(r'^.+@.*enron.com$',recipient)):
                        recipient_mail = recipient
                        if recipients_names!=[]:
                            try:
                                recipient = user.objects.get(inEnron = 1, name=recipients_names[index])
                            except django.core.exceptions.ObjectDoesNotExist:
                                recipient = user(inEnron = True)
                                recipient.save()
                        else:
                            recipient = user(inEnron = True)
                            recipient.save()

                        recipient_mail = mail_address(address = recipient_mail, user_id = recipient.id)
                        recipient_mail.save()
                    
                    #sinon le destinataire est exterieur à enron et on regarde si l'envoyeur est chez enron
                    elif sender.inEnron :
                        recipient_mail = recipient
                        if recipients_names!=[]:
                            try:
                                recipient = user.objects.get(inEnron = 0, name=recipients_names[index])
                            except django.core.exceptions.ObjectDoesNotExist:
                                recipient = user(inEnron = False)
                                recipient.save()
                        else:
                            recipient = user(inEnron = False)
                            recipient.save()

                        recipient_mail = mail_address(address = recipient_mail, user_id = recipient.id)
                        recipient_mail.save()
                    
                    #si sender n'est pas d'Enron et que le destinataire ne l'est pas non plus
                    else:                #on n'a pas de raison de garder une trace de cette communication
                        recipient = None                            
                
                if recipient is not None:
                    current_mail = mail(
                        mailbox_id = current_mailbox.id,
                        date = date,
                        subject = subject,
                        sender_mail_id = sender_mail.id,
                        recipient_mail_id = recipient_mail.id,
                        response = response
                    )
                    if recipients_names!=[]:
                        recipient.name = recipients_names[index]
                    recipient.save()
                    current_mail.save()

            
            ### fin de l'injection des informations
        ### fin de la lecture du mail
