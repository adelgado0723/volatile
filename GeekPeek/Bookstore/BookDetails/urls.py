from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name ='index'),
        path('BooksByAuthor/', views.books_by_author, name ='BooksByAuthor'),

]


