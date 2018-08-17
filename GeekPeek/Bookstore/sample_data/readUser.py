import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *
from django.contrib.auth.models import User as AuthUser

data = csv.reader(open("USER.csv"),delimiter=",")

firstline = True
for row in data:
	if firstline:
		firstline = False
		continue

	print("Reading USER model ...")

	user = USER()

	user.ProfileID=row[0]
	print("ProfileID = " + user.ProfileID)

	# Reading AuthUserID
	print("Reading AuthUser_ID")
	au = AuthUser.objects.get(id=int(row[1]))
	user.AuthUser_ID = au
	print("Printing au: " + str(au))

	# Reading User Home Address...
	usrHomeAddrList = USER_HOME_ADDRESS.objects.filter(Address_ID=row[2]) 
	if usrHomeAddrList:
		usrHomeAddr = usrHomeAddrList[0]

		if usrHomeAddr:
			user.Home_address_ID = usrHomeAddr;
	else:
		print("No home address match!")
		usrHomeAddr = USER_HOME_ADDRESS()
		usrHomeAddr.Address_ID = int(row[2])
		usrHomeAddr.save()
		user.Home_address_ID=usrHomeAddr
	print("Home_address_ID = " + str(user.Home_address_ID.Address_ID))

	# Reading Preferred Credit Card...
	pccList = PREFERRED_CREDIT_CARD.objects.filter(PCC_ID=row[3]) 
	if pccList:
		pcc = pccList[0]

		if pcc:
			user.Preferred_credit_card_ID = pcc;
	else:
		pcc = PREFERRED_CREDIT_CARD()
		pcc.PCC_ID = int(row[3])
		pcc.save()
		user.Preferred_credit_card_ID=pcc
	print("Preferred_credit_card_ID = " + str(user.Preferred_credit_card_ID.PCC_ID))


	# Reading Cart...
	print("Reading Cart...")
	cartList = CART.objects.filter(Cart_ID=row[4]) 
	if cartList:
		cart = cartList[0]

		if cart:
			user.Cart_ID = cart
	else:
		cart = CART()
		cart.Cart_ID = row[4]
		cart.save()
		user.Cart_ID=cart
	print("Cart_ID = " + str(user.Cart_ID.Cart_ID))

	print("Printing user..." + str(user))

	print("Attempting to save...")
	user.save()
	print("Done saving...")

	
	print("USER read SUCCESSFUL")

	#Reading nickname
	print("Reading nickname...")
	nickname = row[5]
	user.Nick_name = nickname

	user.save()	
