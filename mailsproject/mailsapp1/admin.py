from django.contrib import admin
from .models import mailbox,mail_address,mail

admin.site.register(mailbox)
admin.site.register(mail_address)
admin.site.register(mail)