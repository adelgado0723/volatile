from django.urls import path
from . import views

app_name = "myCart"
urlpatterns = [
    path('', views.index, name='index'),
    path('myCart/', views.index, name="myCart"),
    path('changeQuantity/', views.cart_quantity_change, name="changeQuantity"),
    path('removeCartItem/', views.cart_item_remove, name = "removeCartItem"),
    path('deleteSFLitem/', views.delete_SFL_item, name = "delete_SFL_item"),
    path('moveCartItemToSFL/', views.move_cart_item_to_SFL, name = "moveCartItemToSFL"),
    path('moveSflToCart/', views.move_sfl_item_to_cart, name="moveSflToCart"),
    path('addItem/', views.add_item, name ="add_item"),
    path('checkout/', views.checkout, name = "checkout"),
    path('confirm_checkout/', views.confirm_checkout, name = "confirm_checkout"),



    #Views for TESTING. IGNORE THESE
    path('createCookieTest/', views.createCookieTest, name="createCookieTest"),
    path('cookieInfo/', views.cookieInfo, name='cookieInfo'),
    path('makeCartCookie/', views.makeCartCookie, name='makeCartCookie'),
    #path('login_page/', views.login_page, name="loginpage"),
    path('homepage/', views.homepage, name="homepage"),
    path('testView1/', views.testView1, name="testView1"),
    path('sessionTest/', views.sessionTest, name="sessionTest"),
    #path('index', views.index2, name = 'index2')
]