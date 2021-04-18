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

#xml file
tree = ET.parse(path + 'employes_enron.xml')
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
    if isinstance(list_of_mails,mail): return list_of_mails
    return max(list_of_mails, key=lambda x: x.mail_date)

############################
data =  "/home/amait/Downloads" # path + r"/employes_enron"
print(data)
#data = path + r"\mailbox"
#Populate mail database
for folder,sub_folder,files in os.walk(data):

    for file in files:
        file_path = os.path.join(folder,file)
        print("\n fp : ",file_path)
        
        #lecture d'un mail
        with open(file_path,'r') as file:
            recipients = []
            header = True
            response = False

            ###### extraction des informations ######
            lines = iter(file.readlines())
            for line in lines:
                if header:
                    if line[:8]=="X-From: ":
                        line = line[8:]

                        if bool(re.match(r'^".+" <.+@.+>.*$', line)):
                            infos = re.split(' ',line)

                            if len(infos)==2:
                                sender_first_name = ''
                                sender_last_name = infos[0][1:-1]
                                sender_mail = infos[1][1:-2]
                            else:
                                sender_first_name = infos[0][1:]
                                sender_last_name = infos[1][:-1]
                                sender_mail = infos[2][1:-2]

                        elif bool(re.match(r'.+@.+$', line)):
                            sender_first_name = ''
                            sender_last_name = ''
                            sender_mail = line[:-1]
                        
                        sender_name = sender_first_name + " "*(sender_first_name!='') + sender_last_name
                    
                    elif line[:6]=="X-To: "  and len(line) > 7:
                        if line [6:30]!='undisclosed-recipients:,':
                            recipients += re.split(', ',line[6:-1])

                    elif line[:6]=="X-cc: " and len(line) > 7:
                        recipients += re.split(', ',line[6:-1])

                    elif line[:7]=="X-bcc: " and len(line) > 8:
                        recipients += re.split(', ',line[7:-1])

                    elif line[:6]=='Date: ':
                        date = convert_date(line[11:-7])

                    elif line[:9] == "Subject: ":
                        subject = line[9:]
                        
                        if subject[:3] == "Re:":
                            response = True

                    elif line[:9] == "X-Folder:":
                        header = False

            ###### injection dans la db ######
            mailbox_tag = re.search(r"\w+-\w",folder).group()
            current_mailbox = mailbox.objects.get(tag=mailbox_tag)

            try:
                sender_mail = mail_address.objects.get(address=sender_mail)  #on récupère l'id de l'envoyeur
                sender = user.objects.get(pk=sender_mail.user_id)

            except django.core.exceptions.ObjectDoesNotExist:                #s'il n'existe pas dans la db, on le crée
                sender = user(inEnron = False, name = sender_name)
                sender.save()
                sender_mail = mail_address(address = sender_mail, user_id = sender.id)
                sender_mail.save()

            for recipient in recipients:
                try:
                    recipient_mail = mail_address.objects.get(address=recipient)    #on récupère l'id de l'envoyeur
                    recipient = user.objects.get(pk=recipient_mail.user_id)
                    
                except django.core.exceptions.ObjectDoesNotExist:
                    #si le destinataire utilise une adresse enron on lui crée un profil utilisateur sans information d'identité   
                    if bool(re.match(r'^.+@.*enron.com$',recipient)):
                        print('ok',recipient)
                        recipient_mail = recipient
                        recipient = user(inEnron = True)
                        recipient.save()
                        recipient_mail = mail_address(address = recipient_mail, user_id = recipient.id)
                        recipient_mail.save()
                    
                    #sinon le destinataire est exterieur à enron et on regarde si l'envoyeur est chez enron
                    elif sender.inEnron :
                        recipient_mail = recipient
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
                        mail_date = date,
                        subject = subject,
                        sender_mail_id = sender_mail.id,
                        recipient_mail_id = recipient_mail.id,
                        response = response
                    )

                    current_mail.save()


            ### fin de l'injection des informations
        ### fin de la lecture du mail
