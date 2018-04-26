# Linux-Server Project

Project URL: [link](http://ec2-35-154-246-104.ap-south-1.compute.amazonaws.com/)
Notes for reviewer:
* IP (Public): `35.154.246.104'
* Project URL: [link](http://ec2-35-154-246-104.ap-south-1.compute.amazonaws.com/)
* SSH PORT: `2200`


* For this we need Apache, git,python, virtual environment,flask, python app dependencies (pip,sqlalchemy), PostgreSQL and other packages required.
  * Steps for installing these packages are illustrated along with configuration and installation steps.s

##Steps.

* Create a new Ubuntu Linux server instance on Amazon Lightsail.
* Launch Amazon Lightsail terminal
    * You must be logged into your AWS account.
    * Visit [link](https://lightsail.aws.amazon.com/) & Create a new instance of Ubuntu.
    * Get your public IP address.
    * Download default key-pair and copy it to the  /.ssh folder.
    * Open your terminal and change the permissions by tping chmod 600 ~/.ssh/key.pem
    * Enter Command `ssh -i ~/.ssh/key.pem ubuntu@35.154.246.104` to create instance on your terminal

* Create a new user named grader and give the grader permission to sudo
    * `sudo adduser grader`
    * optional: install finger to check user has been added `apt-get install finger`
    * `finger grader`
    * `sudo visudo`
    * In the file add: `grader   ALL=(ALL:ALL) ALL` below root user under "#User privilege specification" and save the file.
    * Add grader to `/etc/sudoers.d/` and type `grader   ALL=(ALL:ALL) ALL` by executing the command `sudo nano /etc/sudoers.d/grader`
    * Add root to `/etc/sudoers.d/` and type `root   ALL=(ALL:ALL) ALL` by executing the command `sudo nano /etc/sudoers.d/root`


* Update all the currently installed packages
    * To Find updates use the command :`sudo apt-get update`
    * Install updates use the command :`sudo apt-get upgrade`

* Changing the SSH port , Disabling `Root login` & implementing `key based authentication`
    * Run the following commands:
    ```
    grader@ip-address:~$ sudo nano /etc/ssh/sshd_config
    ```
    * Find port and add `port 2200` below `port 22`
    * Find `PermitRootLogin prohibit-password` and change it to `PermitRootLogin no` to diable root login
    * Change `PasswordAuthentication` from `no` to `yes`.
    * save file(nano: `ctrl+x`, `Y`, Enter)
    * restart ssh service`sudo service ssh reload`


* Create the SSH keys and copy them to the server manually:

    * On your local machine generate the SSH key pair by: `ssh-keygen`
    * Save the youkeygen file in your ssh directory `/home/ubuntu/.ssh/`.
    * Change the SSH port number in Amazon lightsail to 2200.
    * login into grader account using password by `ssh -v grader@*Public-IP-Address* -p 2200`
    * Create .ssh directory`mkdir .ssh`
    * Create a file to store key`touch .ssh/authorized_keys`
    * On your local machine read the contents of public key `cat .ssh/item.pub`
    * Copy and paste the key in the file you just created (authorized_keys)
    * Set permissions: `chmod 700 .ssh` `chmod 644 .ssh/authorized_keys`
    * Now Changeback `PasswordAuthentication` from `yes` to `no`.  in `nano /etc/ssh/sshd_config` and save.
    * login with key pair: `ssh grader@Public-IP-Address* -p 2200 -i ~/.ssh/item`


* Configure UFW to allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123) only
    * Check UFW status by `sudo ufw status` that it's inactive
    * Deny all the incoming by default & Allow outgoing by default using: `sudo ufw default deny incoming` & `sudo ufw default allow outgoing` respectively
    * Allow SSH `sudo ufw allow ssh`
    * Allow SSH on port 2200, HTTP on port 80 & NTP on port 123 using `sudo ufw allow 2200/tcp` , `sudo ufw allow 80/tcp` & `sudo ufw allow 123/udp` respectively.
    * Turn on UFW using `sudo ufw enable`


* Update the timezone to UTC
    * Run `sudo dpkg-reconfigure tzdata` from prompt and select none then UTC.


* Install and configure Apache to serve Python mod_wsgi application
    * `sudo apt-get install apache2`
    * `sudo apt-get install libapache2-mod-wsgi`
    * Verify wsgi is enabled `sudo a2enmod wsgi`


* Install git
    * `sudo apt-get install git`

* Install python app dependencies
    ```
      $ sudo apt-get install python-pip
      $ sudo pip install Flask=0.9
      $ sudo pip install httplib2 oauth2client sqlalchemy psycopg2 sqlalchemy_utils requests
    ```  

* Configure And Enable New Virtual Host
    * Create host config file `sudo nano /etc/apache2/sites-available/catalog.conf`
    * paste the following:

    ```
    <VirtualHost *:80>
      ServerName 35.154.246.104
      ServerAdmin admin@35.154.246.104
      WSGIScriptAlias / /var/www/catalog/catalog.wsgi
      <Directory /var/www/catalog/catalog/>
          Order allow,deny
          Allow from all
      </Directory>
      Alias /static /var/www/catalog/catalog/static
      <Directory /var/www/catalog/catalog/static/>
          Order allow,deny
          Allow from all
      </Directory>
      ErrorLog ${APACHE_LOG_DIR}/error.log
      LogLevel warn
      CustomLog ${APACHE_LOG_DIR}/access.log combined
  </VirtualHost>
```
    * Save file
    * Enable `sudo a2ensite catalog`

* Create wsgi file
    * `cd /var/www/catalog`
    * `sudo nano catalog.wsgi`

    ```
  #!/usr/bin/python
  import sys
  import logging
  logging.basicConfig(stream=sys.stderr)
  sys.path.insert(0,"/var/www/catalog/")

  from catalog import app as application
  application.secret_key = 'Add your secret key'
  ```

  * Save file

  * Restart apache : `sudo service apache2 restart`

* Clone Github Repository
    * `sudo git clone https://github.com/jabhay97/fullstack_udacity`
    * `shopt -s dotglob`.
    * Move files from clone directory to catalog: `mv /var/www/fullstack_udacity/final_item_catalog/* /var/www/catalog/catalog/`
    * Delete clone directory `sudo rm -r fullstack_udacity`

* Install all used packages.
    * `source venv/bin/activate`
    * `pip install httplib2`
    * `pip install requests`
    * `sudo pip install --upgrade oauth2client`
    * `sudo pip install sqlalchemy`
    * `pip install Flask-SQLAlchemy`
    * `sudo pip install python-psycopg2`
    If you have used any other packages in your project, install those as well.



* Install and configure PostgreSQL:
    * Install postgres with additional models`sudo apt-get install postgresql-contrib`
    * Change in database_setup1.py `engine = create_engine('postgresql://catalog:db-password@localhost/catalog')` and repeat of product1.py and projects1.py
    * Copy projects1.py file into __init__.py file `mv project.py __init__.py`
    * Add catalog user `sudo adduser catalog`
    * login as superuser`sudo su - postgres`
    * Create user catalog`CREATE USER catalog WITH PASSWORD catalog;`
    * Change role of user catalog to creatDB` ALTER USER catalog CREATEDB;`
    * List all users and roles `\du`
    * Create new DB "catalog" with own of catalog`CREATE DATABASE catalog WITH OWNER catalog;` & Connect to database`\c catalog`
    * Revoke all rights from public, and allow only catalog to perform transactions
    ```
    REVOKE ALL ON SCHEMA public FROM public;
    GRANT ALL ON SCHEMA public TO catalog
    ```
    * Run `python database_setup1.py` `python products1.py`
    * restart apache server `sudo service apache2 restart`

* Run Link on your Browser and your project is deployed successfully

* References:
  - Udacity Classroom.<br>
  - Stackoverflow
