# Company Product Application 

A user of this project can add, edit, and delete products of a particular company.  

# Initializing Database with empty tables:
```
$ python database_setup.py
```
To populate the database with data:
```
$ python products.py
```

Congrats! Now the Database Populated!

```
# Starting Application
To start the application enter:
```
$ python catalog.py
* Running on http://0.0.0.0:5000/
* Restarting with reloader
```

Then, go to you browser and type `https://localhost:5000/

Authentication is handled by Google
# Google Authentication Services
You need to supply a client_secrets.json file. You can create an application to use
Google's OAuth service at <a href="https://console.developers.google.com.">`https://console.developers.google.com`</a>
and add your Client Id in `login.html` for Google LogIn.



## Below is the Main Page: