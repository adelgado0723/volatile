# Geek Peek

## About

*Geek Peek* is an online bookstore in the spirit of the website,
*www.thinkgeek.com*. It was developed over the course of ten weeks, subdivided
into five two-week sprints. Features were distributed to a group of five
developers that worked in a ***Scrum/Agile*** Fashion. We held regular stand-up
meetings as well as weekly planning, review, and retrospective meetings. The
Project Requirements were specified at the onset and the developers left to
schedule the user stories pertaining to their feature.


<hr>

## Features Assigned to Developers

| **Feature**                | **Owner**               |
|----------------------------|-------------------------|
| Book Details               | Andres Delgado          |
| Shopping Cart              | Jorge Costafreda        |
| Profile Management         | Jessica Fernandez-Rubio |
| Book Rating and Commenting | Jonathan Jimenez        |
| Book Browsing and Sorting  | Ian Cuvalay             |


<hr>

## Languages and Technologies:
	
- Python
- Django
- SQLite
- Javascript
- CSS 
- Bootstrap


<hr>

## Demo

![Demo](media/demo.gif?raw=true)

<hr>

## Book Details User Stories



1. ***Feature - Display book name, genre, and publishing info (publisher, release
   date, etc.)***

	- User Story - As a online book shopper, I need to see the basic
	  information about the book to know if I would be interested in
	  reading it. This includes the name of the book, the genre of book
	  that it is, and information about the publisher. This should be
	  displayed neatly somewhere that I can easily scan at a glance.

2. ***Feature -  book cover (which can be enlarged when clicked)***

	- User Story - As an online book shopper, I get a  better "feel" for
	  the content of a book when I look at its cover. An online book store
	  should display the cover of each book. The picture of the cover
	  should be clickable such that it enlarges when I click on it.

3. ***Feature -  author and bio***

	- User Story - As an online book shopper, I find information about
	  books' authors to be useful when making a decision about which book
	  to purchase. If a I can easily access an author's biography, by
	  expanding a text field, I can make a better decision about whether I
	  am likely to enjoy one of their books.

4. ***Feature - book description***

	- User Story - As an online book shopper, I need to have access to a
	  description for each book that tells me about the plot and any
	  notable details surrounding the book and the author (like awards that
	  the book has received).

	  
5. ***Feature - book rating, and comments***

	- User Story - As an online book shopper, I would like to see ratings
	  from previous customers as well as their comments on the book.


6. ***Feature - Hyperlink author's name to a list of other books by the same
   author.***
	
	- User Story - As an online book shopper, I would like to be able to
	  click on an authors name, from the book details page, and see the
	  other books that he/she has written.


<hr>

## Files Pertinent to the Book Details Feature

| **File**                    | **Description**               |
|--------------------------------|-------------------------|
| [Bookstore/BookDetails/views.py](https://github.com/adelgado0723/portfolio/tree/master/GeekPeek/Bookstore/BookDetails/views.py) | Retrieves objects to be used from the database. Calculates book rating. |
| [Bookstore/sample_data/](https://github.com/adelgado0723/portfolio/tree/master/GeekPeek/Bookstore/sample_data/) | Contains .csv files with sample data as well as python scripts to read the files and insert the data into the ***SQLite*** database. |
| [Bookstore/templates/BookDetails/book_details.html](https://github.com/adelgado0723/portfolio/tree/master/GeekPeek/Bookstore/templates/BookDetails/book_details.html) | Given a BOOK object, this page displays the cover, details, comments, rating and information about the author. |
| [Bookstore/templates/BookDetails/books_by_author.html](https://github.com/adelgado0723/portfolio/tree/master/GeekPeek/Bookstore/templates/BookDetails/books_by_author.html) | Given a AUTHOR object, this page displays a list of books by that author. |



