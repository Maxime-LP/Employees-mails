# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#from django.contrib.auth.models import User
from django.db import models
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
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
class user(models.Model):
    
    name = models.CharField(null=True,max_length=80)
    inEnron = models.BooleanField(null=False)
    category = models.CharField(null=True,max_length=40)

    def __str__(self):
        return f"{self.name}, {self.inEnron}, {self.category}"



class mailbox(models.Model):
    
    tag = models.CharField(max_length=40)
    #user = models.ForeignKey(user,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.tag}"


class mail_address(models.Model):
    
    address = models.EmailField(max_length=100)
    box = models.ForeignKey(mailbox, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(user, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address}, {self.box}, {self.user.name}"


class mail(models.Model):
    
    mailbox = models.ForeignKey(mailbox,null=True,on_delete=models.CASCADE,related_name='+')
    date = models.DateTimeField(null=True)
    subject = models.CharField(max_length=60,null=True)
    sender_mail = models.ForeignKey(mail_address,null=True,on_delete=models.CASCADE,related_name='sender_mail_id')
    recipient_mail = models.ForeignKey(mail_address,null=True,on_delete=models.CASCADE,related_name='recipient_mail_id')
    response = models.BooleanField(null=True)

    def __str__(self):
        return self.date, self.sender_mail, self.recipient_mail, self.subject, self.response