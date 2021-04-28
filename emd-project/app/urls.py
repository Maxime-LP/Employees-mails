# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
    # The home page
    re_path(r'^$', views.index, name='home'),
    re_path(r'employees', views.employees, name='employees'),
    re_path(r'couples', views.couples, name='couples'),
    re_path(r'days', views.days, name='days'),
    re_path(r'profiles', views.profiles, name='profiles'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
