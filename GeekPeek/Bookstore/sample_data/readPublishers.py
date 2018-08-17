import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

data = csv.reader(open("PUBLISHER_INFO.csv"),delimiter=",")

firstline = True

for row in data:
	if firstline:
		firstline = False
		continue

	print("Reading PUBLISHER_INFO model ...")
	pubInfo = PUBLISHER_INFO()

	pubInfo.PublisherID=int(row[0])
	print("Publisher ID = " + str(pubInfo.PublisherID))

	pubInfo.Name=row[1]
	print("Name = " + pubInfo.Name)

	pubInfo.save()
	print("PUBLISHER_INFO read SUCCESSFUL")



