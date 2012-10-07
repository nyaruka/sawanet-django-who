Who AppFog / Sawanet App
==========================

This is a very simple Django application that demonstrates creating an SMS endpoint for Sawanet. (http://www.sawanet.com)

The application allows users to send in messages in the format ```who [person name]``` and receive a brief summary from the Wikipedia page for that person.

Example queries::

    who michael jackson
    who sting
    who museveni

Getting Started
-----------------

First create a directory to work in and move into it::

    % mkdir smsproject
    % cd smsproject

Now download the git repo into the ```who``` directory::
 
    % git clone git://github.com/nyaruka/sawanet-django-who.git who

Create a virtual environment.  Note AppFog doesn't like virtual environments to be in the same directory as the app, so you have to create this in the ```smsproject``` directory::

    % virtualenv env
    % source env/bin/activate

Now install the dependencies::

    % cd who
    % pip instal -r requirements.txt

Then sync the database::
   
    % python manage.py syncdb

And start the server::

    % python manage.py runserver

You should be able to test the application at ```http://localhost:8000```


Installing at Appfog
---------------------

You'll first need to create an account on http://appfog.com/ and download the appfog utility programs.  Then create a Django application using the AppFog web interface, naming it whatever you'd like.  You can then upload your application::

    % af login
    % af update who   <-- replace who with your app name




