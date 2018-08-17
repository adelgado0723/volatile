import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from django.contrib.auth.models import User

data = csv.reader(open("AUTH_USER.csv"),delimiter=",")
firstline = True

for row in data:
	if firstline:
		firstline = False
		continue

	print("Reading AUTH_USER.csv file...")

	password = row[1]

	username= row[4]

	is_staff = row[7]

	email = row[6]

	print("password: " + password + ", username: " + username + ", email: " + email)
	user = User.objects.create_user(username, email, password)
	
	if is_staff == '1':
		user.is_staff = 1
	else:
		user.is_staff = 0

	print("User info: " + str(user))

	user.save()

	print("AUTH_USER saved successfully")

