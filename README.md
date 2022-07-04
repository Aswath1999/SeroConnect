# SeroConnect
## Introduction
Most of us have gone through periods of stress, anxiety, loneliness and depression. During those challenging times, many of us 
would have wished to have someone to talk to or just a confirmation that we are not alone. SeroConnect was basically created with those particular users in mind.
It provides users with a forum that enables them to talk about their problems freely and even anonymously. SeroConnect has podcasts and videos that speaks about 
mental health and advices the user on how they can handle their problems better. 
## Technologies
### IDE
- Visual Studio Code
### Frontend
- HTML5, CSS3 And JavaScript
- Bootstrap 5
- jQuery
- htmx
### Backend
- Python
- Flask- A Python Micro-Framework
- SqlAlchemy for creating and updating database
- Other packages can be found in the requirements.txt file

## Features
- CRUD (Create/Read/Update/Delete) on Posts by users
- CRUD (Create/Read/Update/Delete) on Comments by users
- Anonymous posts by users
- Registration with confirmation emails
- Reset password emails
- Pagination on posts with Flask-paginate and infinite scrolling with htmx requests
- Pagination on comments with infinite scrolling

## Getting started
- Clone the project from Github  
`https://github.com/Aswath1999/SeroConnect.git`
- Create virtual environment  
`virtualenv venv`  
`venv/bin/activate`  
- Install dependencies from requirements.txt file.  
`pip install -r requirements.txt`. 
- Create a .env file. Setup email configurations in config.py and variables in .env file.
- SeroConnect has gmail configurations. To set it up quickly, create variables `GMAIL=Your Gmail` and  `PASSWORD=Your password` in your .env file. Generate app password from gmail if you have two-factor verification setup.
- Run main.py to run the application
- Check main.py for admin email address and password. A sample user id and password is also given
## Collaborators
 - Gokulvasan https://github.com/gkvzn
 - Vishva  https://github.com/vishvaTHD
## Licensing
MIT
