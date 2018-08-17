import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

data = csv.reader(open("AUTHOR.csv"),delimiter=",")

firstline = True

for row in data:
	if firstline:
		firstline = False
		continue

	print("Reading AUTHOR model ...")
	
	author = AUTHOR()
	author.AuthorID= row[0]
	print("Author ID = " + author.AuthorID)
	
	author.Bio=row[1]
	print("Bio = " + author.Bio)
	
	author.Lname=row[2]
	print("Lname = " + author.Lname)
	
	author.Fname=row[3]
	print("Fname = " + author.Fname)
	
	author.save()
	print("AUTHOR read SUCCESSFUL")
