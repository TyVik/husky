[![Build Status](https://travis-ci.org/TyVik/husky.svg?branch=master)](https://travis-ci.org/TyVik/husky)
[![Coverage Status](https://coveralls.io/repos/github/TyVik/husky/badge.svg)](https://coveralls.io/github/TyVik/husky)
[![Python versions](https://img.shields.io/badge/python-3.5%2C%203.6-blue.svg)](https://github.com/TyVik/husky)


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
3. Install requirements via ```pip install -r requirements.txt```
4. Run ```python3 manage.py runserver 0.0.0.0:8000```
5. Go to [http://127.0.0.1:8000](http://127.0.0.1:8000)

# Admin panel

Administrator can manipulate with quizzes throught [admin panel](127.0.0.1:8000/admin/). For example:

* Add new quiz
* Add question to quiz in quiz detail screen
* Add answers in question detail screen (at least one answer must be marced as correct)
* View users statistic in quiz result list screen (via filter by user or quiz)

# Technical note

For simplification all user progress are store into session. It means that user can open a quiz on many devices, but he can finish only once.

# Текст задания

Задание сформулировано довольно широко, что позволит Вам продемонстрировать знания.

Необходимо создать сервис проведения тестирования. Тесты имеют определенный порядок вопросов. У вопроса может быть один или несколько вариантов правильных ответов, пропуск вопросов не допускается.
Пользователь должен пройти регистрацию или авторизоваться, чтобы приступить к тестированию. Зарегистрированный пользователь может пройти любой тест, после завершения теста видит результат, количество правильных/неправильных ответов и процент правильных ответов. Тест можно пройти только один раз.
Администратор может редактировать любой из тестов и добавлять новые. Посмотреть статистику по пользователю.

* Результат должен быть выложен на GitHub
* Должен запускаться на Python 3.5 и Django 1.11 или более поздних версиях.
* Список всех зависимостей должен храниться в requirements.txt, соответственно можно установить их командой pip install -r requirements.txt.
* По фронту требований никаких не предъявляется. Интерфейс не будет оцениваться.
