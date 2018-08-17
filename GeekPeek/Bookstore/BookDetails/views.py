from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from database.models import BOOK, COMMENT, BOOK_RATING, AUTHOR



# Given a BOOK object, returns a "Book Details" page.
def index(request):
    
    template = loader.get_template('BookDetails/book_details.html')
    if request.method=='GET':
        book = request.GET.get('book')
    if not book:
        book = "9780261103283"
    

    book = BOOK.objects.get(ISBN=str(book))
    comments = COMMENT.objects.filter(ISBN = book)

    rating = BOOK_RATING.objects.get(ISBN = book)
    
    # Taking an average of the ratings values stored 
    # in the database for the given BOOK object. 
    total_ratings = (rating.One_star_count + rating.Two_star_count + rating.Three_star_count + rating.Four_star_count + rating.Five_star_count)
    
    # Avoiding divide by zero issue
    # Integer division behavior
    if not total_ratings == 0:
        average_rating = ((rating.One_star_count * 1 ) + (rating.Two_star_count * 2 ) + (rating.Three_star_count * 3 ) + (rating.Four_star_count * 4 ) + (rating.Five_star_count * 5 )) / total_ratings
        average_rating = round(average_rating) 
    else:
        average_rating = 0

    

    # If no book found, set book found render an error
    context = { 'book':book, 'comments':comments, 'rating':average_rating, 'range': range(average_rating), 'n_filled_range': range(5 - average_rating) }
    

    return HttpResponse(template.render(context, request))


# Given an AUTHOR object returns "Books By Author" page.
def books_by_author(request):

    template = loader.get_template('BookDetails/books_by_author.html')
    author = None
    if request.method=='GET':
        author = request.GET.get('author')
        author = AUTHOR.objects.get(AuthorID=author)

    books = BOOK.objects.filter(AuthorID = author)
    context = { 'author':author, 'books':books, }
    
    return HttpResponse(template.render(context, request))

