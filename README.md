# Book Search and review website

Web Programming with Python and JavaScript - The project is to showcase my coding skills.
"# web50-projects-2020-project1" 

The project uses the flask framework to create a book review website. Database is postgresql. 

Following technologies are used: ## Python, Flask, SQLalchemy, ninja 2, html and css.
The site also use the goodreads API to display the review counts for a particular book.

# templates:

layout.html: This is the html base template imported by all other html files

index.html : This files is the homepage, allow the user to login

registration.html: Displays form to register new user

search.html: Displays the book search functionality when the user successfully logs in the application

book.html: Displays the details about the book, when the user clicks on title on the search page

error.html: displays the error message

# application.py
This file has the following functions:

Registration: Users should be able to register for your website, providing (at minimum) a username and password.

Login: Users, once registered, should be able to log in to your website with their username and password.

Logout: Logged in users should be able to log out of the site.

Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!

Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.

Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.

Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.

API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.
  
# import.py
Import: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from your web application, write a program that will take the books and import them into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.

# create.sql
This contains the definition of the tables that are required for this project

# requirement.txt
This file contains the dependency which need to be pre-installed prior to running this project
