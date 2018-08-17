import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

data = csv.reader(open("PREFERRED_CREDIT_CARD.csv"),delimiter=",")

firstline = True

for row in data:
	if firstline:
		firstline = False
		continue

	print("Reading PREFERRED_CREDIT_CARD model ...")
	pcc = PREFERRED_CREDIT_CARD()

	pcc.PCC_ID=int(row[0])
	print("PCC_ID = " + str(pcc.PCC_ID))

	# Reading Credit Card ...
	ccList = CREDIT_CARD.objects.filter(C_card_number=row[1]) 
	if ccList:
		cc = ccList[0]

		if cc:
			pcc.C_card_number = cc
	else:
		cc = CREDIT_CARD()
		cc.C_card_number = row[1]
		cc.save()
		pcc.C_card_number=cc
	print("C_card_number = " + pcc.C_card_number.C_card_number)

	pcc.save()
	print("PREFERRED_CREDIT_CARD read SUCCESSFUL")
