# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

#from django.contrib.auth.models import User
from django.db import models


#modèle 2
class User(models.Model):
  
    name = models.CharField(null=True, max_length=100)
    inEnron = models.BooleanField(null=False)
    category = models.CharField(null=True, max_length=40)

    def __str__(self):
        return f"{self.name}, {self.inEnron}, {self.category}"


class mailAddress(models.Model):
    
    address = models.EmailField(max_length=200)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address}, {self.user.name}"


class Mail(models.Model):
    enron_id = models.CharField(max_length=120)
    date = models.DateTimeField(null=True)
    subject = models.CharField(max_length=200,null=True)
    sender = models.ForeignKey(mailAddress,null=True,on_delete=models.CASCADE,related_name='sender')
    recipient = models.ForeignKey(mailAddress,null=True,on_delete=models.CASCADE,related_name='recipient')
    isReply = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.date}, {self.sender}, {self.recipient}, {self.subject}, {self.isReply}"