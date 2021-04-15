import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from django.utils.timezone import datetime, timedelta, make_aware, timezone
from app.models import mailbox, mail_address, mail
import xml.etree.ElementTree as ET
import re

##################################################

#path = r'/home/amait/Documents/enron-mails/'
path = r'C:\Users\lepau\OneDrive\Desktop'
"""
###Populate mailbox and mail_address databases
#uncomment to populate

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

data = path + r"\mailbox"
#Populate mail database
for folder,sub_folder,files in os.walk(data):

    for file in files:
        file_path = os.path.join(folder,file)
        print("\n fp : ",file_path)
        
        #lecture d'un mail
        with open(file_path,'r') as file:
            recipients = []
            header = True
            forwarded = False
            response = False

            ###### extraction des informations ######
            lines = iter(file.readlines())
            for line in lines:
                if header:
                    if line[:4]=="To: " or line[:4]=="Cc: " or line[:5]=="Bcc: ":
                        recipients += re.split(', |,',line[4:-1])
                        line = next(lines)

                        while line[0]=="	":
                            recipients += re.split(', |,',line[1:-1])
                            line = next(lines)
                        recipients = [rec for rec in recipients if rec!=""]
                    
                    if line[:6]=='Date: ':
                        date = convert_date(line[11:-7])

                    elif line[:6]=='From: ':
                        sender = line[6:-1]

                    elif line[:9] == "Subject: ":
                        subject = line[9:]
                        
                        if subject[:3] == "Re:":
                            response = True

                        elif line[:4] == "Fwd:":
                            forwarded = True

                    elif line[:7] == "X-From:":
                        header = False


            ###### injection dans la db ######
            mailbox_tag = re.search(r"\w+-\w",folder).group()
            current_mailbox = mailbox.objects.get(tag=mailbox_tag)

            try:
                sender_id = mail_address.objects.get(address=sender).id  #on récupère l'id du mail de l'envoyeur
            except django.core.exceptions.ObjectDoesNotExist:
                sender_id = None                                        #sauf si le mail provient d'une adresse exterieure 
                                                                            #(ou d'un mail pas dans la db)

            for recipient in recipients:

                try:
                    recipient_id = mail_address.objects.get(address=recipient).id       #on récupère l'id du mail du destinataire
                except django.core.exceptions.ObjectDoesNotExist:
                    recipient_id = None                                                 #sauf si le mail va vers une adresse exterieure

                try:
                    #on regarde s'il existe déjà un mail correspondant dans la db (si on l'a créé pour stocker une réponse par exemple)
                    current_mail = mail.objects.get(sender_mail = sender_id, recipient_mail = recipient_id, mail_date = date)
                except django.core.exceptions.ObjectDoesNotExist:
                    current_mail = mail()
                
                current_mail.subject = subject
                current_mail.mail_date = date
                current_mail.mailbox_id = current_mailbox.id
                current_mail.recipient_mail_id = recipient_id
                current_mail.sender_mail_id = sender_id
                current_mail.save()

                ### traitement de la "chaîne" de mails ###
                if response :
                    #on regarde si le mail precédent a déjà été créé
                    previous_mail = mail.objects.filter(sender_mail = recipient_id,recipient_mail = sender_id,
                                                            subject__endswith = subject[3:], mail_date__lt=date)
                    if len(previous_mail)==0:
                        #sinon on le crée
                        previous_mail = mail()
                        previous_mail.sender_mail_id = recipient_id
                        previous_mail.recipient_mail_id = sender_id
                        previous_mail.save()

                    previous_mail = get_most_recent_mail(previous_mail)
                    current_mail.previous_mail_id = previous_mail.id
                    previous_mail.next_mail_id = current_mail.id
                    previous_mail.save()

                else:
                    current_mail.previous_mail = None

                current_mail.save()
            
            ### fin de l'injection des informations
        ### fin de la lecture du mail
                

