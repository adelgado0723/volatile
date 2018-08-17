import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

data = csv.reader(open("CART.csv"),delimiter=",")

firstline = True

for row in data:
	if firstline:
		firstline = False
		continue
	print("Reading CART model ...")
	cart = CART()
	
	cart.Cart_ID=row[0]
	print("Cart_ID = " + cart.Cart_ID)
	
	cart.save()
	print("CART read SUCCESSFUL")

