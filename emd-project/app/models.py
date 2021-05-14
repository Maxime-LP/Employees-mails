# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#from django.contrib.auth.models import User
from django.db import models


class User(models.Model):
  
    name = models.CharField(max_length=100,unique=True,null=False,null=False)
    inEnron = models.BooleanField(,null=False)
    category = models.CharField(max_length=40,null=False)
    '''
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='name_unique')
        ]
    '''
    def __str__(self):
        return f"{self.id}, {self.name}, {self.inEnron}, {self.category}"


class mailAddress(models.Model):
    
    address = models.EmailField(max_length=200, unique=True,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    '''
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['address'], name='address_unique')
        ]
    '''

    def __str__(self):
        return f"{self.id}, {self.address}, {self.user.name}"


class Mail(models.Model):
    enron_id = models.CharField(max_length=30, primary_key=True)
    date = models.DateTimeField(null=False)
    #subject = models.CharField(max_length=750,null=True)
    sender = models.ForeignKey(mailAddress,on_delete=models.CASCADE,related_name='sender',null=False)
    recipient = models.ForeignKey(mailAddress,on_delete=models.CASCADE,related_name='recipient',null=False)
    isReply = models.BooleanField(,null=False)

    def __str__(self):
        return f"{self.enron_id}, {self.date}, {self.sender.address}, {self.recipient.address}, {self.subject}, {self.isReply}"