# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import usr,mailbox,mail_address,mail

admin.site.register(usr)
admin.site.register(mailbox)
admin.site.register(mail_address)
admin.site.register(mail)
