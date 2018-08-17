from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from database.models import CART
from database.models import CART_CONTENT
from database.models import BOOK
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from django.contrib.sessions.models import Session

from . import utility
#test
from django.contrib.auth.models import User
from database.models import USER, SAVED_FOR_LATER_CONTENT
def index(request):
    print("View [index] was called.")
    context = {}
    cart_id = ''
    
    if request.user.is_authenticated: #treat as logged in user
        print("User is logged in.")
        auth_user_id = request.user.id
        print("auth_user_id is: " + str(auth_user_id))
        print(type(auth_user_id)) 

        auth_user = User.objects.get(id = auth_user_id)
        user = USER.objects.get(AuthUser_ID = auth_user_id)

        cart_id = user.Cart_ID.Cart_ID
        saved_for_later_content_list = SAVED_FOR_LATER_CONTENT.objects.filter(ProfileID=user.ProfileID)
        print("saved_for_later_content_list: " + str(saved_for_later_content_list))

        cart = CART.objects.get(Cart_ID = cart_id)
        print("cart is: " + str(cart))

        cart_content_list = cart.cart_content_set.all()
        print("cart_content_list is: " + str(cart_content_list))

        context = {
            'cart_content_list': cart_content_list,
            'cart_content_list_length': len(cart_content_list),
            'Cart_ID': cart_id,
            'subtotal': utility.subtotal(cart),
            'saved_for_later_content_list': saved_for_later_content_list,
            'saved_for_later_content_list_length': len(saved_for_later_content_list),
            'form': forms.QuantityChangeForm(), #used to change quantity of an item
        }
        
        return render(request, 'myCart/index.html', context = context)

    else: #treat as anonymous user
        CART_COOKIE_NAME = 'CartID'
        if CART_COOKIE_NAME in request.COOKIES:            
            print(CART_COOKIE_NAME + " is a valid cookie name.")
            cart_cookie_value = request.COOKIES[CART_COOKIE_NAME]
            print("cart_cokie_value is: " + str(cart_cookie_value))

            print("call Z1")
            cart = CART.objects.all().get(Cart_ID = cart_cookie_value)
            print(cart)
            
            print("Creating cart_content_list")
            cart_content_list = cart.cart_content_set.all()

            print("Printing: CART_CONTENT.objects.filer(cart_id = cart_cookie_value)")
            print(CART_CONTENT.objects.filter(Cart_ID = cart_cookie_value))

            #DON'T FORGET TO DELETE THIS --- TESTT 
            #print("overriding cart and cart_content_list for testing")
            #cart = CART.objects.get(Cart_ID = 'RKV8igMqYPF5EE46bvSyTLQXQKwytyxh') #this cart id actually exists in DB
            #cart = CART.objects.get(Cart_ID = 'blimNAdztSuJWS4kn5NakPArzYIBW5gS')
            #print("Using CartID: RKV8igMqYPF5EE46bvSyTLQXQKwytyxh")
            #cart_content_list = cart.cart_content_set.all()
            #print("override cart_content_list: " +str(cart_content_list))
            #DON'T FORGET TO DELETE THIS --- TESTT
            
            context = {
                'cart_content_list': cart_content_list,
                'cart_content_list_length': len(cart_content_list),
                'Cart_ID': cart_cookie_value,
                'subtotal': utility.subtotal(cart),
                'saved_for_later_content_list': None, #None because saved for later feature is for logged in users only
                'saved_for_later_content_list_length': 0,
                'form': forms.QuantityChangeForm(), #used to change quantity of an item
            }
            
            print("subtotal is: " + str(utility.subtotal(cart)))
            
            return render(request, 'myCart/index.html', context = context) #convert to redirect?
        else:
            #The session does not contain a reference to a cart! Let's create a cart for the anonymous user.
            print("The " + CART_COOKIE_NAME + " was NOT found.")
            print("Creating a " + CART_COOKIE_NAME + " cookie...")
            
            cart_cookie_value = utility.generate_Cart_ID()
            cart = CART(Cart_ID = cart_cookie_value)
            cart.save()
            
            print("Done creating cookie.")
            
            
            #Take the visitor back to this same page. They should have a sessionid and cookie now
            #if user has cookies disabled, this could be infinite loop!
            response = HttpResponseRedirect(reverse("myCart:index", args=None))

            print("Setting the response cookie.")
            response.set_cookie(CART_COOKIE_NAME, cart_cookie_value)
            

            print("response.cookies is: " + str(response.cookies))
            
            return response

    return HttpResponse("Check CMD, something went wrong!")




from . import forms
from . import utility
#This index changes the quantity of a CART_CONTENT tuple
#The information on what tuple, and what the new quantity
# should be is specified in the POST information from the
# request.
def cart_quantity_change(request):
    print("Called [cart_quantity_change2] view")
    
    if request.method == "POST":
        form = forms.QuantityChangeForm(request.POST)

        print("checking if valid:")

        print(request.POST)

        if form.is_valid():
            print("form is valid")
            print("Printing form: " + str(form))
            cart_content_id = form.cleaned_data['Cart_contentID']
            new_quantity = form.cleaned_data['New_quantity']
            utility.change_cart_quantity(cart_content_id=cart_content_id, new_quantity=new_quantity) #use object or 404
            return HttpResponseRedirect(reverse('myCart:index', args=None))
        else:
            print("form is invalid")
            return Http404("Invalid form!")

    else:
        print("Not POST!")
        return Http404("Expected POST: request is not POST")

    return HttpResponse("Uhh read CMD")

#remove an item from a cart
from django.contrib.auth.models import User
from .forms import ItemRemoveForm
from database.models import CART_CONTENT
def cart_item_remove(request):
    print("View [cart_item_remove] called.")
    if request.method == "POST":
        print("Is POST")
        form = ItemRemoveForm(request.POST)
        print(request.POST)

        if form.is_valid():
            print("form is valid")
            print("Printing form: " + str(form))

            cart_content_id = form.cleaned_data['Cart_contentID']
            
            c = None
            try:
                #c = CART_CONTENT().objects.get(Cart_contentID=cart_content_id)
                c = CART_CONTENT.objects.get(Cart_contentID = cart_content_id)
            except CART_CONTENT.DoesNotExist:
                c = None
                raise Http404("Cart item does not exist!")

            print("deleting: " + str(c))
            c.delete()

            print("deleted successfully")
            
            return HttpResponseRedirect(reverse("myCart:index", args=None))
        else:
            print("The form to remove a content item was invalid.")
            raise Http404("The form to remove content item was invalid.")
    else:
        raise Http404("Request to remove cart item was not POST. Must be post and valid form.")
    


def delete_SFL_item(request):
    print("called view: [delete_SFL_item]")
    form = DeleteSFLForm(request.POST)
    print("form is: " + str(form))

    if form.is_valid():
        print("form is valid")
        Saved_ContentID = form.cleaned_data['Saved_ContentID']

        sfl = None
        try:
            sfl = SAVED_FOR_LATER_CONTENT.objects.get(Saved_ContentID = Saved_ContentID)
            print("sfl chosen for deletion is: " + str(sfl))
            sfl.delete()
        except SAVED_FOR_LATER_CONTENT.DoesNotExist:
            raise Http404("Can't delete this saved for later item because it doesn't exist")

        print("Saved for later item deleted")
        return HttpResponseRedirect(reverse("myCart:index", args=None))
    else:
        return HttpResponse("The form to delete a Saved For Later item was invalid!")


def move_cart_item_to_SFL(request):
    print("called view: [move_cart_item_to_SFL]")
    form = MoveCartItemToSFLForm(request.POST)
    print("form is: " + str(form))

    if form.is_valid():
        print("form is valid")
        Cart_contentID = form.cleaned_data['Cart_contentID']
        

        cc = None #user's cart content object to be transfered to saved for later
        user = None #user 
        sfl = None #saved for later object linked to the user

        try:
            cc = CART_CONTENT.objects.get(Cart_contentID = Cart_contentID)
        except CART_CONTENT.DoesNotExist:
            raise Http404("Can't move cart item because item doesn't exist")

        try:
            user = USER.objects.get(Cart_ID = cc.Cart_ID )
        except USER.DoesNotExist:
            raise Http404("Can't move cart item because can't find a link to a user from the Cart_contentID")
        
        try:
            sfl = SAVED_FOR_LATER_CONTENT(ProfileID = user, ISBN = cc.ISBN)
        except SAVED_FOR_LATER_CONTENT.DoesNotExist:
            raise Http404("Can't create a SAVED_FOR_LATER_CONTENT object")


        print("Saving sfl and deleting cc...")
        sfl.save()
        cc.delete()
        print("Done deleting and saving.")
       
        return HttpResponseRedirect(reverse("myCart:index", args=None))
    
    return HttpResponse("Invalid form input: <br>"+str(form.errors))
    

def move_sfl_item_to_cart(request):
    print("View [move_sfl_item_to_cart] was called.")
    form = MoveSflToCartForm(request.POST)
    
    saved_for_later_content = None #saved for later content that will later be deleted
    user = None #user linked to by the sfl
    cart = None #cart to transfer sfl to
    cart_content = None #the content that will be transfered to the cart

    if form.is_valid():
        Saved_contentID = form.cleaned_data['Saved_contentID']

        try:
            saved_for_later_content = SAVED_FOR_LATER_CONTENT.objects.get(Saved_ContentID = Saved_contentID)
            user = saved_for_later_content.ProfileID
            cart = user.Cart_ID
            isbn = saved_for_later_content.ISBN
            
            print("isbn is: " + str(isbn))

            cart_content = CART_CONTENT(ISBN = isbn,Cart_ID=cart, Quantity=1)
            print("cart_content is: " + str(cart_content))
            
        except SAVED_FOR_LATER_CONTENT.DoesNotExist:
            raise Http404("Tryed to instantiate a saved for later object but couldn't")

        print("Saving cart_content and deleting saved_for_later_content...")
        cart_content.save()
        saved_for_later_content.delete()
        print("Done saving and deleting.")

        return HttpResponseRedirect(reverse("myCart:index", args = None))
    else:
        raise Http404("Form invalid:<br>" + str(form.errors))


'''
Adds an item to a cart via a form of AddItemForm
'''
def add_item(request):
    print("Called [add_item]")
    form = AddItemForm(request.POST)
    
    if request.user.is_authenticated: #user logged in. add item to default cartID
        print("[add_item]: User is logged in")

        auth_user = None
        print("getting auth_user...")
        auth_user = request.user
        print("auth_user is: " + str(auth_user))

        user = None
        print("Getting user...")
        user = auth_user.user #user is now an object of USER model since one-to-one relationship
        print("user is: " + str(user))
        
        cart = None
        print("Getting cart...")
        cart = user.Cart_ID
        print("cart is: " + str(cart))
        
        if form.is_valid:
            print("form is valid.")
            ISBN = request.POST['ISBN']

            print("Getting book...")
            book = BOOK.objects.get(ISBN = ISBN)
            print("book is: " + str(book))
        
            print("Creating CART_CONTENT object referecing this cart...")
            cart_content = CART_CONTENT(ISBN=book, Cart_ID = cart, Quantity=1)
            print("cart_content is: " + str(cart_content))

            print("Saving cart_content...")
            cart_content.save()
            print("Done saving cart_content.")
            
            return HttpResponseRedirect(reverse("myCart:index", args=None))
        else:
            print("form is invalid.")
            raise Http404("Form data to add item into cart was invalid.")
        return HttpResponseRedirect(reverse("myCart:index", args=None))
    else:
        '''User is anonymous. Add item to cart specified by cart cookie. If user doesn't have a cookie yet,
        then set one for the user'''
        print("User is anonymous")

        CART_COOKIE_NAME = 'CartID'

        if CART_COOKIE_NAME in request.COOKIES:
            print("User has a cookie with the name: " + CART_COOKIE_NAME)
            #user is anonymous and a cookie has already been set, great!

            cart_cookie_value = request.COOKIES[CART_COOKIE_NAME]

            cart = None
            cart_content = None
            book = None

            if form.is_valid():
                cart = CART.objects.get(Cart_ID=cart_cookie_value)
                isbn = form.cleaned_data["ISBN"]
                book = BOOK.objects.get(ISBN = isbn)
                cart_content = CART_CONTENT(ISBN = book, Cart_ID = cart, Quantity=1)
                
                cart_content.save()

                context = {"book" : book}

                return render(request, "myCart/itemAddedResponse.html", context=context)
            else:
                raise Http404("Form was invalid!")

            return HttpResponse("You're an anonymous user, and you have a CartID cookie.<br>You got here which is great <br> This function part of the branchwill be implemented later.")
            #IMPLEMENT HERE
        else:
            #user is anonymous but does not have a cookie for the cart, let's create one.
            print("Anonymous user does not yet have a cookie for the cart. Creating one now")
            cart_id = utility.generate_Cart_ID()
            print("Will eventually send back a cookie named CART_COOKIE_NAME with the value of "+str(cart_id))
           

            print("Let's create the CART object before we send back to request to the user.")
            cart = CART(Cart_ID = cart_id)
            print("Saving cart...")
            cart.save()
            print("Done saving cart.")

            if form.is_valid:
                print("form is valid.")

                ISBN = request.POST["ISBN"]
                print("ISBN is: " + str(ISBN))

                book = BOOK.objects.get(ISBN = ISBN)
                print("book is: " + str(book))
                
                print("Creating CART_CONTENT object...")
                cart_content = CART_CONTENT(ISBN = book, Cart_ID = cart, Quantity=1)
                cart_content.save()
                print("cart_content is: " + str(cart_content))
                
                context = {'book': book}
                response = render(request, "myCart/itemAddedResponse.html", context)
                response.set_cookie(CART_COOKIE_NAME, cart_id)

                print("Printing response.cookies: " + str(response.cookies))
                
                return response
            else:
                raise Http404("Form data to add item into cart was invalid.")

        return HttpResponseRedirect(reverse("myCart:index", args=None))


def checkout(request):
    shipping_addresses = []
    reserved_credit_cards = [] #RESERVED_CREDIT_CARD objects that belong to the user
    addresses = [] #ADDRESS objects that belong to user (loaded from shipping_addresses array)
    credit_cards = [] #CREDIT_CARD objects that belong to user (loaded later on from reserved_credit_cards array)
    items = [] #loaded with CART_CONTENT objects
    user = None
    authuser = None
    cart = None
    subtotal = 0
    
    
    #default credit card is the card that is used by default to make payments.
    #since the default credit card hasn't been implemented yet, we will just pick the default to be the
    #first credit card in the list of credit cards that are saved to a users account.
    default_credit_card = None 
    card_last_four = None #last four digits of default credit card

    context = {}

    if request.user.is_authenticated:
        authUser = request.user
        user = authUser.user
        reserved_credit_cards = user.reserved_credit_card_set.all()
        cart = user.Cart_ID
        items = cart.cart_content_set.all()
        subtotal = utility.subtotal(cart)
        shipping_addresses = user.user_shipping_address_set.all()

        for rcc in reserved_credit_cards:
            credit_cards.append(rcc.C_card_number)

        if credit_cards:
            default_credit_card = credit_cards[0]
            card_last_four = utility.get_last_four_digits_credit_card(credit_cards[0])

        #get the items
        items = cart.cart_content_set.all()
        print("items -> " + str(items))
        subtotal = utility.subtotal(cart)
        print("subtotal -> " + str(subtotal))

        #set default shipping address to first address in list if not empty
        default_address = None
        if shipping_addresses:
            default_address = shipping_addresses[0].Address_ID

        context = {
            #"cart" : cart,
            "items" : items,
            "subtotal" : subtotal,
            #"shipping_addresses" : shipping_addresses,
            #"reserved_credit_cards" : reserved_credit_cards,
            "default_credit_card" : default_credit_card,
            "default_address" : default_address,
            #"credit_cards" : credit_cards,
            "card_last_four" : card_last_four,
        }

        for key in context:
            print("key: " + str(key) + " -- value: " + str(context.get(key)))
    else:
        #User not logged in, what do we do?
        print("")


    print("[checkout] view called.")
    return render(request, "myCart/checkout.html", context = context)

@login_required
def confirm_checkout(request):
    authUser = request.user
    user = authUser.user
    cart = user.Cart_ID

    items = cart.cart_content_set.all()

    for item in items:
        print("Would remove: " + str(item))
    
    items.delete()

    return render(request, 'myCart/confirm_checkout.html', context=None)



#--------------------------------------------------------------------
#----------------TEST INDEXS BELOW, IGNORE THESE---------------------
#--------------------------------------------------------------------
#test
def run_this_instead_1():
    sess = Session.objects.get(pk='cm8sb17zrk4defbq8kkj20zo703ne53c')
    print(type(sess))
    print("Undecoded: " + sess.session_data)
    print(type(sess.session_data))
    print("Decoded: " + str(sess.get_decoded()))
    print(type(sess.get_decoded()))

    #print("-------------------------")
    #sess = Session.objects.get(pk='486wo45e0h5tinb6as9pqr4juwgrcu9h')
    #print("Coded: " + sess.session_data)
    #print("Decoded: " + str(sess.get_decoded()))
    
    return HttpResponse("Read CMD")


#test
def cartItemInfo(Cart_ContentID):
    return ""

def myCart(request):
    print("View [myCart] was called.")
    return render(request, 'myCart/myCartSimple.html')

def index3(request):
    return HttpResponse("HELLO WORLD!")

def consoleSessionDisplay(request):    
    for key, value in request.session.items():         
        print('{} => {}'.format(key, value))
    return HttpResponse("Check command promt for session information!")

def makeCookieTest(request):
    return ""

def makeCookieWorkedTest(request):
    ""

def indexTest(request):
    '''
    posts = Post.objects.all()[0:10]  
    

    context = {
        'title': 'Latest Posts',
        'posts': posts
    }

    
    return render(request, 'post/index.html', context)
    '''    
    
    return HttpResponse('Just text :[')#
    #return render(request, 'myCart/index.html')


from database.models import GENRE
def example2(request):
    all_genre=GENRE.objects.all()
    template = loader.get_template('myCart/example.html')
    context = {'all_genre':all_genre}
    #return render(request, 'myCart/example.html')
    return HttpResponse(template.render(context, request))


def createCookieLogin(request):
    return ""


from django.http import HttpResponse
from django.shortcuts import render
def createCookieTest(request):
    if request.session.test_cookie_worked():        
        #the cookie worked, let's get information
        #about the session to see if we can find the cookie
        html = "<h1>Test Cookie Worked!<h1><br>"
        html += "<h3>Here's some information about the session: <h3><br>"

        for key in request.session.keys():
            html+=("Session key: "+str(key)+"<br>&emsp;:=> request.session["+str(key) +"]: "+str(request.session[key])+"<br>")
        
        html+="<br> Now I'm going to delete it!"
        
        
        request.session.delete_test_cookie()        
        return HttpResponse(html)
    else:
        request.session.set_test_cookie()        
        return HttpResponse("Test cookie failed or no test cookie set yet"
        "<br>Please reload this page.")
    

def createCookieTest2(request):
    """
    if request.method == 'POST':
        if request.session.test_cookies_worked():
            print("The test cookie worked!")
            return HttpResponse("You're logged in.")
        else:
            return HttpResponse("Please enable cookies and try again.")
    
    print("Request method was not POST. setting up a test cookie!")
    request.session.set_test_cookie()
    """
    
    return HttpResponse("No form detected, setting up a test cookie.")

#http://localhost:8000/myCart/cookieInfo
def cookieInfo(request):
    if request.COOKIES.get("sessionid") is not None:
        print("sessionID was found! It is: "+request.COOKIES.get("sessionid"))
    else:
        print("There was so sessionID cookie!")
        
    return HttpResponse("Done, check CMD for feedback")

'''Creates a CartID cookie used by the Cart. '''
#http://localhost:8000/myCart/makeCartCookie
from database.models import CART
import datetime
def makeCartCookie(request):
    print("Creating cookie CartID...")    

    #Before we continue, if the user already had a CartID cookie
    #   then don't create a new one. Instead just leave their CartID
    #   cookie how it is.
    for key in request.session.keys():
        print(key+" :=> "+request.session.get(key))

    if request.session.get("sessionid"):
        print("There was a session key in request.session")
    else:
        print("There was no session key in request.session...")

    if request.session.get("CartID"):
        print("There was a CartID in request.session")
    else:
        print("There is no CartID in request.session")

    if 'CartID' in request.COOKIES:
        print("In request.COOKIES there is a CartID")
        print("The CarID is: " + request.COOKIES['CartID'])
    else:
        print("In request.COOKIES there is no CartID")

    if request.session.get("CartID") is None:
        print("No CartID cookie detected in client. Creating one now.")
                      
        #generate a random string 32 chars long
        val = CART.generate_Cart_ID()
        print("Value generated is: "+val)

        #set the cookie
        response = HttpResponse("")
        max_age=86400 #1 day
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie('CartID', val, max_age=86400, expires=expires)
                
        response.write("<h1>Cookie has been set</h1>")
        print("Cookie has been set.")

        return response
    else:
        print("The request already has a CartID cookie.")
        print("The value of the cookie is: "+request.session.get("CartID"))

        return HttpResponse("A cookie had already been set. It will not be changed.")


''' not being reference in myCart/urls.py'''
from django.contrib.auth import authenticate, login
def login_page_info(request):
    
    print("Got here")   
    username = request.POST['user']    
    password = request.POST['pwd']

    user = authenticate(request, username=username, password=password)

    if user is None:
        print("Invalid user info")
        return HttpResponse("Invalid user info")
    else:
        print("That was a valid user")
        return HttpResponse("Invalid user info")

def homepage(request):
    return render(request, 'myCart/homepage.html', {})


#test    
def indexOLD(request): 
    #response = HttpResponseRedirect(reverse('index', args=None))
    #shortcut(response)
    
    
    print("View [index] was called.")
    COOKIE_NAME = 'CartID'
    context = {}
    Cart_ID = ''

    #problems: if user has cookies disabled, might be infinite loop
    if COOKIE_NAME in request.COOKIES:
        print(COOKIE_NAME + " is a cookie in the request")
        print("The value of "+COOKIE_NAME+" is: "+request.COOKIES[COOKIE_NAME])
        
        cookieValue = request.COOKIES[COOKIE_NAME]        

        #Search every cart until we find a match
        for cart in CART.objects.all():
            if cart.Cart_ID == cookieValue: #We've found a match
                print("The cookie's value matches a Cart_ID value of a CART object")                
                #Success! Load the page!
                print("TEST:"+str(cart.Cart_ID)+" length = "+str(len(cart.Cart_ID)))

                cart_content_list = cart.cart_content_set.all()
                print("cart_content_list contains: "+ str(cart_content_list))

                context["cart_content_list"] = cart_content_list
                context["Cart_ID"] = cart.Cart_ID

                #create the context later
                print("Context is: "+str(context))        
                return render(request, 'myCart/myCart.html', context=context)
        
        #No match was found in the database
        #   Do: 1)Create cookie  2)Store Data in CART DB table  3)Set the cookie on the response
        print("The cookie value DOES NOT match any Cart_ID value in the CART table")

        
        
        #response = HttpResponseRedirect(reverse('errorpage', args=None))
        #response.delete_cookie('CartID')
        #do nothing for now
        return HttpResponse("ERROR")
                
    else:
        ''' there was no CartID associated with the session, make one, \
            update the DB and then reload the page'''
        
        #This response's cookie will be set below
        response = HttpResponseRedirect(reverse('index', args=None))
        
        print("CartID is not a cookie in the request. Making a cookie now.")
        
        
        
        #max_age = 86400 #Remove this CartID after it has been the the DB for 7 days
        
        #generate a cookie value
        cookie_value = CART.generate_Cart_ID()
        print("Generated a cookie, the value is: "+cookie_value+" setting the key/value pair now.")
        response.set_cookie("CartID", cookie_value)         
        print("Done setting cookie")
        print("Done creating cookie, redirecting user now.")

        print("Creating a cart")
        c = CART()
        value = c.generate_Cart_ID() #generater random string of len 32 via static function
        c.Cart_ID = value
        c.save()
        print("Done creating a cart.")
        
        #test - for not just set it to sometthing that has a lot of items
        
        response.set_cookie('CartID','xGwiiFrlmh4cl8DW7MBH5Cm8XmU0i2n0')

        print("Reloading page.")
        #reload the page now that the cookie has been set
        return response 

#test
# Description: 
#   Utility function.
#   Assigns the request a CartID cookie with a randomly generated string as its value.
#       the generated string is 32 chars long.
#   When it is done, it redirects the user back to a page.
# Input: 
#   request-HttpRequest who's cookie will be set
#   cookie_value-The value that you want the CartID cookie to be set to
# Output:
#
def createCookieAndCart(request, cookie_value=""):    
    print("Setting a cookie for the user. Adding ")
    cookie_value=CART.generate_Cart_ID()
    c = CART()
    value = cookie_value
    c.Cart_ID = value
    c.save()
    request.set_cookie("CartID", cookie_value)
    return ""#test

#test
#Lets person view cart. Uses session instead of login.
def indexOLD2(request):
    print("View [index] was called.")
    SESSION_COOKIE_NAME = 'sessionid'
    CART_COOKIE_NAME = 'CartID'
    cart_cookie_value = ''

    #ignore this
    print("Calling: request.session.session_key")
    print(request.session.session_key)
    print("Calling: request.session.__contains__(SESSION_NAME)")
    print(request.session.__contains__(SESSION_COOKIE_NAME)) #why return false?
    
    print("Calling: request.session")
    print(request.session)
       

    
    #Check if the session contains a CART_COOKIE_NAME cookie
    if CART_COOKIE_NAME in request.session:
        print(CART_COOKIE_NAME + " is a valid cookie name for this session.")
        cart_cookie_value = request.session[CART_COOKIE_NAME]
        print("cart_cokie_value is: " + str(cart_cookie_value))

        #return HttpResponse("A Session was found info:<br>Session_name: %s<br>Session_value%s:"%(SESSION_NAME, str(session_value)))        

        print("call Z1")
        cart = CART.objects.all().get(Cart_ID = cart_cookie_value)
        print(cart)
        
        print("Creating cart_content_list")
        cart_content_list = cart.cart_content_set.all()

        print("Printing: CART_CONTENT.objects.filer(Cart_ID = cart_cookie_value)")
        print(CART_CONTENT.objects.filter(Cart_ID = cart_cookie_value))

        #DON'T FORGET TO DELETE THIS --- TESTT 
        print("overriding cart and cart_content_list for testing")
        cart = CART.objects.get(Cart_ID = 'RKV8igMqYPF5EE46bvSyTLQXQKwytyxh') #this cart id actually exists in DB
        print("Using CartID: RKV8igMqYPF5EE46bvSyTLQXQKwytyxh")
        cart_content_list = cart.cart_content_set.all()
        print("override cart_content_list: " +str(cart_content_list))
        #DON'T FORGET TO DELETE THIS --- TESTT
        
        context = {
            'cart_content_list': cart_content_list,
            'cart_content_list_length': len(cart_content_list),
            'Cart_ID': cart_cookie_value,
            'subtotal': utility.subtotal(cart),
            'form': forms.QuantityChangeForm(), #used to change quantity of an item
        }

        print("subtotal is: " + str(utility.subtotal(cart)))
        

        #return HttpResponse("This session had a cookie for "+CART_COOKIE_NAME+".<br>"+
        #"the value of that cookie is: " + cart_cookie_value)

        #response = response.session.__setitem__("sessionIDDDD", "wakka wakka")        
        
        return render(request, 'myCart/index.html', context = context)
    else:
        print("The " + CART_COOKIE_NAME +" was NOT found.")
        print("Creating a " + CART_COOKIE_NAME + " cookie...")
        
        utility.create_cart_id_value(request)
        print("Done creating cookie.")

        #Take the visitor back to this same page. They should have a sessionid and cookie now
        #if user has cookies disabled, this could be infinite loop
        return HttpResponseRedirect(reverse('myCart:index', args=None))

    return HttpResponse("Check CMD")

from django.contrib.sessions.backends.db import SessionStore
def sessionTest(request):
    
    
    print((request.session))
    print(type(request.session))
    print((request.session.session_key))

    print(request.session.decode()) #print server side cookies
    
    #run_this_instead_1()
    return HttpResponse("Check CMD")
    

def testView1(request):
    return render(request, 'myCart/testView1.html', context = {})