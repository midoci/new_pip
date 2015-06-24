#!/usr/bin/env python  
# coding: utf-8  
  
import os  
  
os.environ['DJANGO_SETTINGS_MODULE'] = 'summer_2015.settings'  
  
#import django.core.handlers.wsgi  
#application = django.core.handlers.wsgi.WSGIHandler() 
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
