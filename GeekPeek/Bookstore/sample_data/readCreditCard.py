import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

data = csv.reader(open("CREDIT_CARD.csv"),delimiter=",")

firstline = True

for row in data:
	if firstline:
		firstline = False
		continue

	print("Reading CREDIT_CARD model ...")
	cc = CREDIT_CARD()
	
	cc.C_card_number=row[0]
	print("C_card_number = " + cc.C_card_number)
	
	cc.CVV=row[1]
	print("CVV = " + cc.CVV)
	
	cc.Exp_day=row[2]	
	print("Exp_day = " + cc.Exp_day)
	
	cc.Exp_month=row[3]	
	print("Exp_month = " + cc.Exp_month)
	
	cc.Exp_year=row[4]	
	print("Exp_year = " + cc.Exp_year)
	
	cc.Fname=row[5]	
	print("Fname = " + cc.Fname)
	
	cc.Lname=row[6]	
	print("Lname = " + cc.Lname)
	
	cc.Mname=row[7]	
	print("Mname = " + cc.Mname)
	
	cc.save()
	print("CREDIT_CARD read SUCCESSFUL")
