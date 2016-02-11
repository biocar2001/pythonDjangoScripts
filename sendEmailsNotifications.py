import os
import sys
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

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from validate_email import validate_email
''' this script build and send emails to your users, you could execute this script every X time for sending emails specific users who has specific parameters'''
print 'START SEND OF EMAILS:::::::::::'
lista_noti = NotificacionEmail.objects.filter(send=False)
# Send the message via local SMTP server.
s = smtplib.SMTP("server.adress.smtp",25)
for message in lista_noti:
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = message.subject
	msg['From'] = message.emailFrom
	msg['To'] = message.emailTo
	#--------In this case I am builing an url for redirection in the email	
	url_modulo = ""
	titulo_email = ""
	descripcion_email = "" 
	titular=""
	if message.tipo == "1":
		url_modulo ="/one/" + str(message.IdAuxiliar)
		try:
			sopo = OneObjetc.objects.get(pk=message.IdAuxiliar)
			titulo_email = sopo.titulo 
			descripcion_email = sopo.descripcion
			solucion_email = sopo.solucion
			if solucion_email == '':
				solucion_email = "Campo sin informar"
			estado_email = sopo.get_OneObjetc_display()
			titular="One"
		except:
			#Exception
			titulo_email = "Ir al detalle del Registro" 
			descripcion_email = "Ir al detalle del Registro"
			solucion_email = "Ir al detalle del Registro"
			estado_email = "Ir al detalle del Registro"
			titular="OneObjetc"
		messageHTML = message.mensaje + " " + settings.DEMAT_URL_SERVICE + str(url_modulo) 
		t = loader.get_template('templates/templateEmail1.html')
		c = Context({'mensaje': messageHTML, 'tituloHTML':titulo_email, 'descripcion_email':descripcion_email,'solucion_email':solucion_email,'estado_email':estado_email, 'titular':titular })
		html = t.render(c)

	elif message.tipo == "2":
		url_modulo ="/two/" + str(message.IdAuxiliar)
		try:
			docu = twoObjetcs.objects.get(pk=message.IdAuxiliar)
			titulo_email = docu.nombre 
			descripcion_email = docu.comentario
			titular="two"
			comentario_email = docu.comentarioLittle
			if comentario_email == '':
				comentario_email = "Campo sin informar"
			estado_email = docu.get_two_display()
		except:#Exception en caso de ser una notificacion del sistema en cuyo caso no hay ID del registro para enviar
			titulo_email = "Ir al detalle del Registro" 
			descripcion_email = "Ir al detalle del Registro"
			titular="two"
			comentario_email = "Ir al detalle del Registro"
			estado_email = "Ir al detalle del Registro"
		messageHTML = message.mensaje + " " + settings.DEMAT_URL_SERVICE + str(url_modulo) 
		t = loader.get_template('templates/twoObjetcs.html')
		c = Context({'mensaje': messageHTML, 'tituloHTML':titulo_email, 'descripcion_email':descripcion_email,'comentario_email':comentario_email,'estado_email':estado_email, 'titular':titular })
		html = t.render(c)

	elif message.tipo == "3":
		url_modulo = "/three/" + str(message.IdAuxiliar)
		try:
			uti = threeObjects.objects.get(pk=message.IdAuxiliar)
			titulo_email = uti.nombre 
			descripcion_email = uti.descripcion
			titular="threeObjects"
			comentario_email = uti.comentarioLittle
			if comentario_email == '':
				comentario_email = "Campo sin informar"
			estado_email = uti.get_estadoUtil_display()

		except:#Exception en caso de ser una notificacion del sistema en cuyo caso no hay ID del registro para enviar
			titulo_email = "Ir al detalle del Registro" 
			descripcion_email = "Ir al detalle del Registro"
			titular="threeObjects"
			comentario_email = "Ir al detalle del Registro"
			estado_email = "Ir al detalle del Registro"
		messageHTML = message.mensaje + " " + settings.DEMAT_URL_SERVICE + str(url_modulo) 
		t = loader.get_template('templates/threeObjects.html')
		c = Context({'mensaje': messageHTML, 'tituloHTML':titulo_email, 'descripcion_email':descripcion_email,'comentario_email':comentario_email,'estado_email':estado_email, 'titular':titular })
		html = t.render(c)

	elif message.tipo == "4":
		url_modulo = "/four/" + str(message.IdAuxiliar)
		try:
			fourobjects = fourobjects.objects.get(pk=message.IdAuxiliar)
			titulo_email = fourobjects.nombre 
			descripcion_email = fourobjects.asunto
			titular="fourobjects"
		except:#Exception en caso de ser una notificacion del sistema en cuyo caso no hay ID del registro para enviar
			titulo_email = "Ir al detalle del Registro" 
			descripcion_email = "Ir al detalle del Registro"
			titular="fourobjects"
		messageHTML = message.mensaje + " " + settings.DEMAT_URL_SERVICE + str(url_modulo) 
		t = loader.get_template('templates/fourobjects.html')
		c = Context({'mensaje': messageHTML, 'tituloHTML':titulo_email, 'descripcion_email':descripcion_email,'titular':titular })
		html = t.render(c)

	
	
	
	try:
		part1 = MIMEText(html.encode("utf-8"),'html','utf-8')

		msg.attach(part1)
		if message.emailTo is not None:
			s.sendmail(message.emailFrom, message.emailTo, msg.as_string())
			print "EMAIL sent to::::::::::: "
			print message.emailTo 
		else:
			print "EMAIL dont sent to::::::::::: "
			print message.emailTo 
		fecha_hoy = timezone.now()
		message.fechaEnvio = fecha_hoy
		message.enviado = True
		message.save()

	except IOError, e: # or "as" if you're using Python 3.0
		print "EXCEPTION::::::::::: Error sending emails "
		print "Error:", sys.exc_info()[0]
		errorMensaje = "Error :" + str(sys.exc_info()[0])
		messageHTMLErrorProcess = "Error sending Emails\n" + errorMensaje
		tError = loader.get_template('templates/templateEmail.html')
		cError = Context({'mensaje': messageHTMLErrorProcess})
		htmlError = tError.render(cError)
		part1Error = MIMEText(htmlError.encode("utf-8"),'html','utf-8')
		msg.attach(part1Error)
		s.sendmail("Error", ['test@hotmail.com'], msg.as_string())
		break
s.quit() 
print 'END SENDING EMAILS:::::::::::'