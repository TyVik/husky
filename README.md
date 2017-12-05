This demo application is designed for create and solve quizzes. 

* Client side is just HTML pages without any js. 
* Quizzes and questions can be created through the admin panel. 
* User must be authorized for solving. 
* User can solve any quiz only once.

# Installation

This app is Django-application, and next steps may be helpfull for installation:

1. Clone this repository.
2. Create local postgres db with user husky:
```
> sudo su postgres -c psql

postgres=# create user husky with password 'husky';
postgers=# create database husky owner;
```
3. Run ```python3 manage.py runserver 0.0.0.0:8000```
4. Go to [http://127.0.0.1:8000](http://127.0.0.1:8000)

# Admin panel

Administrator can manipulate with quizzes throught [admin panel](127.0.0.1:8000/admin/). For example:

* Add new quiz
* Add question to quiz in quiz detail screen
* Add answers in question detail screen (at least one answer must be marced as correct)
* View users statistic in quiz result list screen (via filter by user or quiz)

# Technical note

For simplification all user progress are store into session. It means that user can open a quiz on many devices, but he can finish only once.
