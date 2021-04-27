# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#from django.contrib.auth.models import User
from django.db import models

""" #modèle 1
class mailbox(models.Model):
    tag = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    category = models.CharField(max_length=40,default='Employee')

class mail_address(models.Model):
    box = models.ForeignKey(mailbox, on_delete=models.CASCADE)
    address = models.EmailField(max_length=80)

class mail(models.Model):
    mail_date = models.DateTimeField(null=True)
    mailbox = models.ForeignKey(mailbox,null=True,on_delete=models.CASCADE,related_name='+')
    recipient_mail = models.ForeignKey(mail_address,null=True,on_delete=models.CASCADE,related_name='recipient_mail_id') #NULL si le mail va à l'exterieur
    subject = models.CharField(max_length=60,null=True)
    sender_mail = models.ForeignKey(mail_address,null=True,on_delete=models.CASCADE,related_name='sender_mail_id') #NULL si le mail provient de l'exterieur
    previous_mail = models.ForeignKey("self",null=True,on_delete=models.SET_NULL,related_name='+')
    next_mail = models.ForeignKey("self",null=True,on_delete=models.SET_NULL,related_name='+')
"""

#modèle 2
class User(models.Model):
    
    name = models.CharField(null=True, max_length=100)
    inEnron = models.BooleanField(null=False)
    category = models.CharField(null=True, max_length=40)

    def __str__(self):
        return f"{self.name}, {self.inEnron}, {self.category}"



class Mailbox(models.Model):
    tag = models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.tag}"


class mailAddress(models.Model):
    
    address = models.EmailField(max_length=200)
    box = models.ForeignKey(Mailbox, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address}, {self.box}, {self.user.name}"


class Mail(models.Model):
    enron_id = models.CharField(max_length=120)
    mailbox = models.ForeignKey(Mailbox, null=True, on_delete=models.CASCADE, related_name='+')
    date = models.DateTimeField(null=True)
    subject = models.CharField(max_length=200,null=True)
    sender = models.ForeignKey(mailAddress,null=True,on_delete=models.CASCADE,related_name='sender_mail_id')
    recipient = models.ForeignKey(mailAddress,null=True,on_delete=models.CASCADE,related_name='recipient_mail_id')
    isReply = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.date}, {self.sender}, {self.recipient}, {self.subject}, {self.isReply}"