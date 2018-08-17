import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

data = csv.reader(open("BOOK_RATING.csv"),delimiter=",")

firstline = True

for row in data:
	if firstline:
		firstline = False
		continue

	print("Reading BOOK_RATING model ...")

	br = BOOK_RATING()

	br.BOOK_RATING_ID = int(row[0])	
	print("Book_Rating_ID = " + str(br.BOOK_RATING_ID))
	
	# Reading ISBN ...
	bList = BOOK.objects.filter(ISBN=row[1]) 
	if bList:
		b = bList[0]

		if b:
			br.ISBN = b;
	else:
		b = BOOK()
		b.ISBN = row[1]
		b.save()
		br.ISBN = b
	print("ISBN = " + br.ISBN.ISBN)

	br.Five_star_count = int(row[2])	
	print("br.Five_star_count = " + str(br.Five_star_count))

	br.Four_star_count = int(row[3])	
	print("br.Four_star_count = " + str(br.Four_star_count))

	br.Three_star_count = int(row[4])	
	print("br.Three_star_count = " + str(br.Three_star_count))

	br.Two_star_count = int(row[5])	
	print("br.Two_star_count = " + str(br.Two_star_count))

	br.One_star_count = int(row[6])	
	print("br.One_star_count = " + str(br.One_star_count))

	br.Zero_star_count = int(row[7])	
	print("br.Zero_star_count = " + str(br.Zero_star_count))


	br.save()
	print("BOOK_RATING read SUCCESSFUL")

