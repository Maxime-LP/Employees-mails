from django.db import models

class mailbox(models.Model):
    tag = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    category = models.CharField(max_length=40,default='Employee')

class mail_address(models.Model):
    box = models.ForeignKey(mailbox, on_delete=models.CASCADE)
    address = models.EmailField(max_length=80)

class mail(models.Model):
    mail_date = models.DateTimeField(null=False)
    recipient_mail = models.ForeignKey(mail_address, on_delete=models.CASCADE,related_name='recipient_mail_id')
    #il peut y avoir plusieurs destinataires
    sender_mail = models.ForeignKey(mail_address, on_delete=models.CASCADE,related_name='sender_mail_id')
    previous_mail = models.ForeignKey("self",null=True,on_delete=models.SET_NULL,related_name='previous_mail_id')
    response_mail = models.ForeignKey("self",null=True,on_delete=models.SET_NULL,related_name='response_mail_id')
    #il peut y avoir plusieurs resp