# Book Review Website

User can do the following:
1. Register, Login, Logout of the website.
2. Search for books based on title, auhtor, isbn
3. Selected book can be reviewed read other people's reviews


PS. One review per user allowed. 


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
