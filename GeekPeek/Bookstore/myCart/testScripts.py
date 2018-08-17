import sys, os, csv, django

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bookstore.settings'
django.setup()

from database.models import *

#Loads a cart with a set of books.
#This method was created for testing the remove function of the cart.
def add_books_into_cart():
    book1 = BOOK.objects.get(pk="246916072-3")
    book2 = BOOK.objects.get(pk="621334348-2")
    book3 = BOOK.objects.all()[4]
    book4 = BOOK.objects.all()[5]
    

    CART_ID = 'RKV8igMqYPF5EE46bvSyTLQXQKwytyxh' #Actually exists in DB. Also one used in myCart's index view

    Cart = CART.objects.get(Cart_ID=CART_ID)

    
    pk = CART_CONTENT.objects.last().Cart_contentID + 1
    print("pk is: " + str(pk))
    cc = CART_CONTENT(Cart_contentID = pk, ISBN = book1, Cart_ID=Cart, Quantity=50)
    cc.save()

    pk = CART_CONTENT.objects.last().Cart_contentID + 1
    print("pk is: " + str(pk))
    cc = CART_CONTENT(Cart_contentID = pk, ISBN = book2, Cart_ID=Cart, Quantity=75)
    cc.save()

    pk = CART_CONTENT.objects.last().Cart_contentID + 1
    print("pk is: " + str(pk))
    cc = CART_CONTENT(Cart_contentID = pk, ISBN = book3, Cart_ID=Cart, Quantity=75)
    cc.save()

    pk = CART_CONTENT.objects.last().Cart_contentID + 1
    print("pk is: " + str(pk))
    cc = CART_CONTENT(Cart_contentID = pk, ISBN = book4, Cart_ID=Cart, Quantity=75)

    cc.save()

    print("DONE!")

def viewLoggedInUsers():
    return None

from django.contrib.sessions.models import Session
def viewSessionData():
    #session_key = 'mjtqvyuakkvw610zeo4rdx7mqj3jqpuj'

    for session in Session.objects.all():
        print("SESSION: " + str(session))
        data = session.get_decoded()
        for key in data:
            print('\t' + str(key) + ": " + data[key])
    
    return None


from database.models import SAVED_FOR_LATER_CONTENT
from database.models import USER
def add_books_into_SFL():
    book1 = BOOK.objects.get(pk="246916072-3")
    book2 = BOOK.objects.get(pk="621334348-2")
    book3 = BOOK.objects.all()[2]
    book4 = BOOK.objects.all()[3]
    
    profile = USER.objects.get(pk=1)

    try:
        pk = SAVED_FOR_LATER_CONTENT.objects.last().Saved_ContentID + 1
    except:
        pk=1

    print(type(pk))

    print("pk is: " + str(pk))

    sflc = SAVED_FOR_LATER_CONTENT(pk=pk, ISBN=book1, ProfileID = profile)

    print("sflc is: " + str(sflc))

    print("saving sflc...")
    sflc.save()
    print("done saving sflc")

    pk = SAVED_FOR_LATER_CONTENT.objects.last().Saved_ContentID + 1
    sflc = SAVED_FOR_LATER_CONTENT(pk=pk, ISBN=book2, ProfileID = profile)
    sflc.save()

    pk = SAVED_FOR_LATER_CONTENT.objects.last().Saved_ContentID + 1
    sflc = SAVED_FOR_LATER_CONTENT(pk=pk, ISBN=book3, ProfileID = profile)
    sflc.save()

    pk = SAVED_FOR_LATER_CONTENT.objects.last().Saved_ContentID + 1
    sflc = SAVED_FOR_LATER_CONTENT(pk=pk, ISBN=book4, ProfileID = profile)
    sflc.save()

    return None



add_books_into_cart()