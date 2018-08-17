''' This python file is used to create helper functions that are  used by the myCart app'''

import random
from django.contrib.auth.models import User as AuthUser
#from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def generate_Cart_ID():
	choice = '0123456789abcdefghijklmnopqrstuvwxyz'
	NUMBERS = 10
	LETTERS = 26
	SIZE = NUMBERS+LETTERS

	cartID = ''

	for i in range(0, SIZE):
		c = random.randint(0, SIZE-1)
		cartID += choice[c]

	return cartID


from database.models import CART
#use this when creating cart cookie for session only
def create_cart_id_value(request):
	print("generating cart_value...")
	cart_value = generate_Cart_ID()
	print("Done, cart_value is: "+cart_value)
	print("Generated value was unique, great!")

	request.session['CartID'] = cart_value #for session cookie only!

	#add cart_value to the CART database
	c = CART(Cart_ID=cart_value)
	c.save()

	return cart_value


from database.models import CART_CONTENT
def change_cart_quantity(cart_content_id,new_quantity):
	print("Called [change_cart_quantity] method. ")	
	
	print("Getting cart content object")
	cc = CART_CONTENT.objects.get(Cart_contentID = cart_content_id)
	
	print("cc is: " + str(cc))

	print("current quantity is: " + str(cc.Quantity))

	print("Changing quantity")
	if new_quantity > 0:
		cc.Quantity = new_quantity
	#cc.Quantity = new_quantity

	print("New Quantity: " + str(cc.Quantity))
	
	print("Saving instance of cart_content")
	cc.save()

	return None


''' not being used atm '''
#Given a CART objects, finds out how many items are in 
#the cart
#Input:
#	CART - Cart objects
#Output:
#	Number of items in the CART objects
def get_num_items_in_cart(CART):
	print("Generating set.")
	cc_set = CART.cart_content_set 

	print("cc_set is: ")
	print(cc_set)

	print("len(cc_set) is: ")
	print(str(len(cc_set)))

	return len(cc_set)

from database.models import CART

#Calculate subtotal price of the items in a CART objects
#input:
#	CART: CART object
#output:
#	sum: sum of the total cost, factoring in quantity as well
def subtotal(CART):
	cart_content_list = CART.cart_content_set.all()
	sum=0

	if cart_content_list is None:
		sum = 0
	else:
		for item in cart_content_list:
			if item.ISBN is None or item.ISBN.Price is None:
				continue
			elif item.Quantity is None:
				continue
			
			if item.Quantity < 0:
				raise ValueError('Quantity is negative. It should be positive!')
			
			sum += (item.Quantity*item.ISBN.Price)
	
	return sum

def get_cart_items(request):
	return None

'''
#Gets all shipping addresses (of type ADDRESS, not SHIPPING_ADDRESS!)
#that belong to a user
#input:
#	request
#output:
#	List of ADDRESS types that belong to the user
@login_required
def get_user_shipping_addresses(request):
	print("method [get_user_shipping_addresses] called")
	authUser = request.user
	shipping_addresses = authUser.shipping_address_set.all()
	addresses = []

	for ship_addr in shipping_addresses:
		print("Address " + str(ship_addr) + "added")
		addresses.append(ship_addr)
		
	return addresses


@login_required
#Gets all reserved credit cards (of type []CREDIT_CARD rather than []RESERVED_CREDIT_CARD)
#input:
#	request
#output:
#	list of CREDIT_CARD types that belong to the user
def get_user_reserved_cards(request):
	print("function [get_user_reserved_cards] called")
	authUser = request.user
	reserved_credit_cards = authUser.reserved_credit_card_set.all()
	credit_cards = []

	for rcc in reserved_credit_cards:
		print(str(rcc) + " was added.")
		credit_cards.append(rcc)

	return credit_cards
'''

#Get the last four digits of a credit card
#input: CREDIT_CARD object
#output: last four digits of the card as a string
def get_last_four_digits_credit_card(CREDIT_CARD):
	if CREDIT_CARD is None:
		return ValueError("CREDIT_CARD object must not be None and have at least four digits.")
	cc_number = CREDIT_CARD.C_card_number
	if len(cc_number) < 4:
		return ValueError("CREDIT_CARD object must not be None and have at least four digits.")
	return cc_number[-4:]