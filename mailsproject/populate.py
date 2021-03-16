import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailsproject.settings')
import django
django.setup()

from mailsapp1.models import mailbox,mail_address,mail
import xml.etree.ElementTree as ET
import zipfile

path = r'C:\Users\lepau\OneDrive\Desktop'

#xml file
tree = ET.parse(path + '\employes_enron.xml')
root = tree.getroot()

###Populating mailbox and mail_address databases
#already populated
"""
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

