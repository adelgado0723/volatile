import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

data = csv.reader(open("USER.csv"),delimiter=",")

firstline = True
for row in data:
	if firstline:
		firstline = False
		continue

	usrHomeAddr = USER_HOME_ADDRESS()


	usrHomeAddr.Home_address_ID=int(row[0])
	print("Home_address_ID = " + str(usrHomeAddr.Home_address_ID))

	# Reading Credit Card ...
	addrList = ADDRESS.objects.filter(Address_ID=row[1]) 
	if addrList:
		addr = addrList[0]

	if addr:
		usrHomeAddr.Address_ID = addr;
	else:
		addr = ADDRESS()
		addr.Address_ID = int(row[1])
		addr.save()
		usrHomeAddr.Address_ID=addr
	print("Address_ID = " + str(usrHomeAddr.Address_ID.Address_ID))

	usrHomeAddr.save()
	print("USER_HOME_ADDRESS read SUCCESSFUL")
