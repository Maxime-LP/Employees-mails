from django.db import models

class employee(models.Model):
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    category = models.CharField(max_length=40,default='Employee')

class mailbox(models.Model):
    tag = models.CharField(max_length=60)
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    mail1 = models.CharField(max_length=60,null=True)
    mail2 = models.CharField(max_length=60,null=True)
    mail3 = models.CharField(max_length=60,null=True)

class mail(models.Model):
    mail_date = models.DateField(null=True)
    recipient_mailbox = models.ForeignKey(mailbox, on_delete=models.CASCADE,related_name='recipient_mailbox_id')
    sender_mailbox = models.ForeignKey(mailbox, on_delete=models.CASCADE,related_name='sender_mailbox_id')
    previous_mail = models.ForeignKey("self",null=True,on_delete=models.SET_NULL,related_name='previous_mail_id')
    response_mail = models.ForeignKey("self",null=True,on_delete=models.SET_NULL,related_name='response_mail_id')
