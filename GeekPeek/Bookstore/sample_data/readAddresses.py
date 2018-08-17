import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

data = csv.reader(open("ADDRESS.csv"),delimiter=",")

firstline = True
for row in data:
	if firstline:
		firstline = False
		continue
	print("Reading ADDRESS model ...")
	addr = ADDRESS()
	
	addr.Address_ID=int(row[0])
	print("Address_ID = " + str(addr.Address_ID))

	addr.Zip_Post=row[1]
	print("Zip_Post = " + addr.Zip_Post)

	addr.Address_1=row[2]	
	print("Address_1  = " + addr.Address_1)

	addr.Address_2=row[3]	
	print("Address_2  = " + addr.Address_2)

	addr.Country=row[4]	
	print("Country  = " + addr.Country)

	addr.State=row[5]	
	print("State  = " + addr.State)

	addr.City_Town=row[6]
	print("City_Town  = " + addr.City_Town)

	addr.Name=row[7]	
	print("Name  = " + addr.Name)


	addr.save()
	print("ADDRESS read SUCCESSFUL")
