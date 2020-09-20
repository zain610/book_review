# Book Review Website

User can do the following:
1. Register, Login, Logout of the website.
2. Search for books based on title, author, isbn
3. Select a book, read and write reviews for the book! 📖


PS. One review per user allowed. 

## Tech Stack
1. Backend and Database
    1. Flask
    2. SQL
    3. SQLAlchemy
    4. GoodReadsAPI
2. Front End
    1. HTML
    2. CSS
    3. Jinja2 ( templating engine )
3. Other -- Designs, Project Managment
    1. Trello
    2. Adobe XD

## Install
make sure you have the python3+ installed
```
pip install -r requirements.txt
```

## Basic API usage
GET request to: <b>/api/isbn/:keyword</b> where keyword is of isbn of the book of your choice.
Given that the book exists in our database, a request like this 
<b>https://book-review-zain.herokuapp.com/api/0425238199</b> should return:
```
{
"author": "Maya Banks",
"average_rating": 2,
"isbn": "0425238199",
"review_count": 3,
"title": "No Place to Run",
"year": 2010
}
```
Thank you for visiting!
