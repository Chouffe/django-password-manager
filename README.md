Password Manager
=======

Enables password Management through one Master Key and via DES 256 encryption
The passwords are encrypted into the DB on the server and only the provided key
when logged in can decrypt them.

Demo here: http://demo-password-manager.herokuapp.com/

- login: test
- password: test


Installation
=======

1. Git clone this repo
2. Add an heroku app

> git heroku git:remote -a app-name

3. Deploy on Heroku

> git push heroku master


DB Config
======

Set up the admin user + password when asked by Heroku
The masterKey used to encrypt the passwords is obtained by hashing your DB
password with a sequence of MD5.
Advice: Use a strong masterKey password to ensure good protection of your
passwords!


Techs used
======

Django is used as the web framework.
Some Javascript (AJAX calls) and Bootstrap (Twitter Bootstrap) are used to enhance the frontend.
TDD is used as the coding philosophy.
