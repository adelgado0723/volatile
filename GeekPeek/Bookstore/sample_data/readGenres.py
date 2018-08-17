import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

data = csv.reader(open("GENRE.csv"),delimiter=",")
firstline = True

for row in data:
	if firstline:
		firstline = False
		continue

	print("Reading GENRE model ...")
	genre = GENRE()
	
	genre.GenreID=row[0]
	print("GENRE ID = " + genre.GenreID)
	
	genre.Name=row[1]
	print("Name = " + genre.Name)
	
	genre.Description=row[2]	
	print("Description = " + genre.Description)
	
	genre.save()
	print("GENRE read SUCCESSFUL")
