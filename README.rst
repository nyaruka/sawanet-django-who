Who AppFog / Sawanet App
------------------------

This is a very simple Django application that demonstrates creating an SMS endpoint for Sawanet. (http://www.sawanet.com)

The application allows users to send in messages in the format ``who [person name]`` and receive a brief summary from the Wikipedia page for that person.

Example::

    >>> who michael jackson
    <<< Michael Joseph Jackson (August 29, 1958 – June 25, 2009) was an American recording artist, entertainer and businessman. Often referred to as the King of Pop, or by his initials MJ, Jackson is recognized as the most successful entertainer of all time by Guinness World Records.

Getting Started
-----------------

First create a directory to work in and move into it::

    % mkdir smsproject
    % cd smsproject

Now download the git repo into the ``who`` directory::
 
    % git clone git://github.com/nyaruka/sawanet-django-who.git who

Create a virtual environment.  Note AppFog doesn't like virtual environments to be in the same directory as the app, so you have to create this in the ``smsproject`` directory::

    % virtualenv env
    % source env/bin/activate

Now install the dependencies::

    % cd who
    % pip instal -r requirements.txt

Then sync the database::
   
    % python manage.py syncdb

And start the server::

    % python manage.py runserver

You should be able to test the application at ``http://localhost:8000``


Installing at Appfog
---------------------

You'll first need to create an account on http://appfog.com/ and download the appfog utility programs.  Then create a Django application using the AppFog web interface, naming it whatever you'd like.  You can then upload your application::

    % af login
    % af update who   <-- replace who with your app name


Configuring on Sawanet
-------------------------

If you have your application running on AppFog, you can make it work with the 8080 shortcode on Sawanet in just a few minutes.  First go to http://www.sawanet.com and create an account by entering your phone number and click "Start Now".

Once you confirm your account details, claim a keyword to use.  You'll do this by sending a message with the keyword you want to the 8080 shortcode::

    claim who    <-- replace with your own keyword

You can now configure your keyword to post incoming messages to your AppFog application.  Go to the configuration page for your keyword and click on the "Receiving Message" tab.  Using the AppFog domain you chose, enter the delivery URL as follows. (in this example, my AppFog domain is ``who.aws.af.cm``::

    http://who.aws.af.cm/sms/receive?text=%(text)s&number=%(number)s

Set the **Delivery Method** to ``POST``, check the box for **Delivery Response**, then click **Save Delivery Settings**.

From that point on anyone will be able to send messages to your Django application using the keyword you picked.




