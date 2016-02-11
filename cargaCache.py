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
''' Load query in cache system like redis'''
from django.core.cache import cache
try:
	#USERS
	users = users.objects.all().order_by('id')
	cache.set('users',users, timeout=None)
except:
	print error