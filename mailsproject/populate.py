import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailsproject.settings')
import django
django.setup()

from mailsapp1.models import employee,mail,mailbox
import xml.etree.ElementTree as ET
import zipfile

path = r'C:\Users\lepau\OneDrive\Desktop'

#csv file
tree = ET.parse(path+'\employes_enron.xml')
root = tree.getroot()

###Populating employee and mailbox databases
"""
for child in root:
    current_employee = employee()
    current_mailbox = mailbox()
    
    try:
        current_employee.category = child.attrib['category']
    except KeyError:
        current_employee.category = 'Employee'

    for subchild in child:
        if subchild.tag == 'lastname':
            current_employee.last_name = subchild.text

        elif subchild.tag == 'firstname':
            current_employee.first_name = subchild.text

        elif subchild.tag == 'email':
            if current_mailbox.mail1 == None:
                current_mailbox.mail1 = subchild.attrib['address']
            elif current_mailbox.mail2 == None:
                current_mailbox.mail2 = subchild.attrib['address']
            elif current_mailbox.mail3 == None:
                current_mailbox.mail3 = subchild.attrib['address']

        elif subchild.tag =='mailbox':
            current_mailbox.tag = subchild.text
    
    current_employee.save()
    current_mailbox.employee_id = current_employee.id
    current_mailbox.save()
"""

