from django.db import models

class employee(models.Model):
    last_name = models.CharField(max_length=40),
    first_name = models.CharField(max_length=40),
    
    #uncomplete choices list
    CATEGORY_CHOICES = [
        ('Employee', 'Employee'),
        ('Director', 'Director')
    ]
    
    category = models.CharField(max_length=40,choices=CATEGORY_CHOICES,default='Employee')

class mailbox(models.Model):
    mail_adress = models.CharField(max_length=60)
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)

class mail(models.Model):
    mail_date = models.DateField(),
    mail_rec = models.ForeignKey(mailbox, on_delete=models.CASCADE),
    mail_exp = models.ForeignKey(mailbox, on_delete=models.CASCADE),
    prec = models.ForeignKey("self",null=True,on_delete=models.SET_NULL),
    resp = models.ForeignKey("self",null=True,on_delete=models.SET_NULL)
