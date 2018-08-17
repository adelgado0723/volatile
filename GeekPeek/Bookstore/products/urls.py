from django.urls import path, include
from products import views

urlpatterns = [
    path('', views.products, name = 'product'),
    path('productsold/', views.productsold, name = 'whatDisPageDo?!'),
]