import os
import sys
import psutil
# When you are working in windos wih Django, you will need add these lines  with the path of your project
# sys.path.append('C:\\djangoprojects\\CARLOS')
# sys.path.append('C:\\djangoprojects')
sys.path.append('C:\\djangoprojects\\PROJECT')
sys.path.append('C:\\djangoprojects')
os.environ['DJANGO_SETTINGS_MODULE'] = "CARLOS.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CARLOS.settings") 

# -*- coding: utf-8 -*-
# Probably you dont need all the libraries here included, but I dot remember what are mandatories for this script.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext,Context, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.context_processors import csrf
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from xlwt import *
from xlrd import open_workbook
from xlutils.save import save
from xlutils.copy import copy
from xlwt.Utils import rowcol_to_cell
from xlutils.styles import Styles
#from simplejson import *
from django.core import serializers
import operator
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import csv
import re
import os
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from validate_email import validate_email
''' this script check the proccess in windows, if some process use maximun memory of 800 MB send an email of information'''
# You can use the script for linux systems too, for example you could check if your apache server is overload or you mongoDB server.
# Email Server
s = smtplib.SMTP("smtp.srver.org",25)
print "Monitoring............."

for proc in psutil.process_iter():
	try:
		pinfo = proc.as_dict(attrs=['pid', 'name'])
	except psutil.NoSuchProcess:
	 	pass
	#if pinfo['name'] == str('httpd*32.exe'):
	# Check memory of process
	p = psutil.Process(pinfo['pid'])
	#print "::::::: Memory used for the proccess ::::::::: " + str(p.name())
	
	memory = p.memory_info()
	
	if memory[1] > 100000 :
		print str(memory[1]/1024) + " KB "
	memory = memory[1]/1024
	
	if memory > 800000:
		# Kill proceso
		# p.terminate()
		# Create message container - the correct MIME type is multipart/alternative.
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'Process with maximun of 800 MB - Check the process'
		msg['From'] = 'AlertSystem'
		msg['To'] = 'test@gmail.com'
		try:
			errorMensaje = "Process with maximun of 800 MB - Check the process"
			part1Error = MIMEText(errorMensaje.encode("utf-8"),'html','utf-8')
			msg.attach(part1Error)
			s.sendmail("Error", ['AlertSystem'], msg.as_string())
		except:
			print "EXCEPTION::::::::::: Error email "
			print "Error:", sys.exc_info()[0]
			

