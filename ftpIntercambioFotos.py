import sys, os, paramiko, datetime
import errno
# When you are working in windos wih Django, you will need add these lines  with the path of your project
# sys.path.append('C:\\djangoprojects\\CARLOS')
# sys.path.append('C:\\djangoprojects')
sys.path.append('C:\\djangoprojects\\PROJECT')
sys.path.append('C:\\djangoprojects')
os.environ['DJANGO_SETTINGS_MODULE'] = "CARLOS.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CARLOS.settings") 

# -*- coding: utf-8 -*-
# Probably you dont need all the libraries here included, but I dot remember what are mandatories for this script.
''' this script is for exchange documents in a FTP server where you save your documents. Its useful in the case of you have a lot machines
with the same app and you need have all the documents in all the machines.'''
from django.conf import settings

try:
	# Configuracion del FTP de destino
	transport = paramiko.Transport((settings.FTP_HOST, settings.FTP_PORT))
	transport.connect(username = settings.FTP_USERNAME, password = settings.FTP_PASSW)

	# Check wich one documents were uploaded
	querysetFotos = fotoftp.objects.filter(subido=False, host= settings.HOST).distinct()
	# connect FTP
	sftp = paramiko.SFTPClient.from_transport(transport)

	print "#######################"
	print "## INIT UPLOAD   ##"
	print "#######################"
	print str(querysetFotos.count())
	countUploads = 0
	# get every one for uploading to FTP
	for foto in querysetFotos:

		# Upload Files 
		local_path = settings.MEDIA_ROOT + '/' + foto.archivoPath # build path for upload
		remote_path = settings.MEDIA_ROOT_FTP + foto.urlPath # path in the ftp server
		name_file = foto.nameFile # Name of file
		#print name_file
		#print local_path
		#print remote_path

		try:
			sftp.chdir(remote_path)  # Check if exist folder in server FTP
		except IOError:
			sftp.mkdir(remote_path)  # Create Folder in ftp server
			sftp.chdir(remote_path)
		try:	
			sftp.put(local_path, name_file) 
		except IOError, e: # or "as" if you're using Python 3.0
				print e
				print " Unexpected error: " + str(sys.exc_info()[0])
				break
		countUploads = countUploads + 1
		foto.subido = True # check as uploaded
		foto.host = settings.HOST # put the form where we upload the file
		foto.save()
		sftp.chdir('/')

	print "#######################"
	print "## FINISH UPLOAD ##"
	print "# "+str(countUploads) +" documents uploaded in FTP from the machine: " + settings.HOST
	print "#######################"
	print "#######################"
	print "## DOWNLOAD STARTED   ##"
	print "#######################"
	# Download Files
	# 
	#Check that files have been uploaded but are not on the table downs associated with the hostname of the current machine
	querysetfotosDownloaded = fotoftp.objects.filter(subido=True).exclude(fotoDownloaded__host = settings.HOST)
	countDownloads = 0
	# we take each of them to get them down to the current machine
	print ":::TOTAL FOR DOWNLOAD::::::::::" 
	print len(querysetfotosDownloaded)
	print ":::::Begin::::::::" 
	for fotoD in querysetfotosDownloaded:
		
		# Download Files 
		remote_path = settings.MEDIA_ROOT_FTP + fotoD.archivoPath # FTP full path to download file
		local_path = settings.MEDIA_ROOT+ "/" + fotoD.urlPath # local path where the file will be saved
		name_file = fotoD.nameFile # Name of the file will be transferred to the server
		#print name_file
		#print local_path
		#print remote_path

		try:
			if not os.path.exists(local_path):
				os.makedirs(local_path)  # We create the directory if FTP does not exist
			os.chdir(local_path)
				
			sftp.stat(remote_path) # check if the file exist
			sftp.get(remote_path, name_file) 
		except IOError, e: # or "as" if you're using Python 3.0
				print e
				print ":::::::::::::::::::::::::::::::::::::::::::"
				print " Unexpected error: " + str(sys.exc_info()[0])
				
				break
		countDownloads = countDownloads + 1
		# We mark the file as downloaded by including it in the table
		fotoDownloaded = fotoDownloadedFtp(host=settings.HOST, nombreArchivo=name_file, fechaBajada=datetime.now())
		fotoDownloaded.save()
		fotoD.fotoDownloaded.add(fotoDownloaded)
		fotoD.save()
		

	print "#######################"
	print "## DOWNLOAD FINISH ##"
	print "#######################"
	print "# " + str(countDownloads) + " Docuemnts downloaded in the machine : " + settings.HOST

	# close ftp connection
	sftp.close()
	transport.close()
	#raise Exception("I know python!")
except:
	print sistemaError
	