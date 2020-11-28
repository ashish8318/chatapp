# Chatapp
# Introduction

This chatapp created with **flask socketio** and **javascripts socket**. This is simple chatapp in which user login then he redirect on chat page or he show message you are connected. In this chat app also provide dashbord in which user create own room, upload own profile photo, send own room to any people who create register in chatapp. user also delete own friend or show all friend. user go on the chat page or select room so in this case message send in a selected room. not show all user that are connected. But user not choose room then in this case message send all user.

# Demo
# File/ Folder in chatpp
  * **application:** This is main file . This file contain createing app instance, database connection, or import all package. This file contain code that handle like registration,login,dashbord, socket connect, join room, leave room or logout functionality.

  * **models:** This file contains class base table structure. This methodlogy called **ORM** in flask. this class covert in table with SQLAlchemy. I also add usermixin in class to appy flask login functinality.

  * **Forms:** I create form with flask_wtf, with flask_wtf create the form with python code then creating instance and render. flask templete engine converted this in simple html form. (This contain userLogin , registration, uploadFile form). This also contain validation of field like InputRequired,Length,Email validation, or email already exists.

  * **Static folder:** This folder contains static image in image folder
  
  * **Templates folder:** This folder contains client page like base.htm login.html, register.html, dashbord.html, chat.html, logout.html. In which chat.html conatin all socket connection , join room, leave room all javascripts code in scripts tag. I use jquery write this code. I use **UI KIT** framwork for html page design.         
# Features of chatapp
  * Email validation with sending email link varification.
  * use ui kit framwork best and faster web page design just like bootstarp.

# Deploy
 I use heroku free host website paltform for testing purpose. I use postgress object oriented database system.
 I use some command:-
 ```
 myenv\scripts\activate.bat
 pip insatll gevent-websocket
 pip install gunicorn
 pip freeze > requirement.txt
 git init
 git add .
 git commit -m '-------'
 heroku login
 git:remote -a 'name of heroku app'
 git push heroku master
 ```
 # Run Chatapp
 My chatapp is host on heroku server. you can visit click on this link :
 [Chat-group](https://mychat-group.herokuapp.com)

 # Refrence 
  * [flask quickstart ](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
  * [flask socketio](https://flask-socketio.readthedocs.io/en/latest/)


