# Linux Server Configuration

	This is to deploy the Investment Catalog in Amazon Lightsail

	IP address  : 52.220.149.210
	Host Name		: ec2-52-220-149-210.ap-southeast-1.compute.amazonaws.com

## Step 1: Setup Amazon Lightsail
		1. Connect using SSH

## Step 2: (Optional) Update all currently installed packages
		1. sudo apt-get update
		2. sudo apt-get upgrade

## Step 3: Configure Lightsail firewall
		1. sudo ufw default deny incoming
		2. sudo ufw default allow outgoing
		3. sudo ufw allow ssh
		4. sudo ufw allow 2200/tcp
		5. sudo ufw allow 22/tcp
		6. sudo ufw allow www
		7. sudo ufw allow 123
		8. sudo ufw enable and answer y
		9. sudo ufw status to check the status

## Step 4. Change the SSH port from 22 to 2200
		1. sudo nano /etc/ssh/sshd_config
		2. Change Port 22 to Port 2200
		3. sudo service ssh restart
		4. add port 2200 under firewall in AWS web

## Step 5. Give grader access
		1. sudo adduser grader
		2. sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader
		3. sudo nano /etc/sudoers.d/grader
		4. change ubuntu to grader
		5. ssh-keygen for grader
		6. sudo mkdir /home/grader/.ssh
		7. sudo touch /home/grader/.ssh/authorized_keys
		8. sudo nano /home/grader/.ssh/authorized_keys
		9. sudo chmod 700 /home/grader/.ssh
		10. sudo chmod 644 /home/grader/.ssh/authorized_keys
		11. sudo chown -R grader:grader /home/grader/.ssh

## Step 6. Change timezone
		1. sudo dpkg-reconfigure tzdata
		2. sudo apt-get install ntp

## Step 7. Install Apache mod_wsgi
		1. sudo apt-get install apache2
		2. sudo apt-get install libapache2-mod-wsgi python-dev
		3. sudo a2enmod wsgi
		4. sudo service apache2 start

## Step 8. Install git
		1. sudo apt-get install git
		2. git config --global user.name "xxxxx"
		3. git config --global user.email "xxxxx@gmail.com"

## Step 9: Clone the Catalog from Github
		1. cd /var/www
		2. sudo mkdir catalog
		3. sudo chown -R grader:grader catalog
		4. git clone https://github.com/sssamwong/investmentCatalog catalog
		6. sudo nano catalog.wsgi

			#!/usr/bin/python
			import sys
			import logging
			logging.basicConfig(stream=sys.stderr)
			sys.path.insert(0,"/var/www/catalog/")

			from catalog import app as application
			application.secret_key = 'super_secret_key'

## Step 10. Install virual environment, Flask and other imports
		1. sudo apt-get install python-pip
		2. sudo pip install virtualenv
		3. cd /var/www/catalog
		4. sudo virtualenv venv
		5. source venv/bin/activate
		6. sudo chmod -R 777 venv
		7. pip install Flask
		8. pip install bleach httplib2 requests oauth2client sqlalchemy
		9. sudo apt-get install python-psycopg2

## Step 11. Configure and enable a new virtual host
		1. sudo nano /etc/apache2/sites-available/catalog.conf
		2. Paste the below lines of codes:

			<VirtualHost *:80>
				ServerName 52.220.149.210
				ServerAdmin admin@52.220.149.210
				ServerAlias ec2-52-220-149-210.ap-southeast-1.compute.amazonaws.com
				WSGIDaemonProcess catalog python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
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

		3. sudo a2ensite catalog

## Step 12. Install and configure PostgreSQL
		1. sudo apt-get install libpq-dev python-dev
		2. sudo apt-get install postgresql postgresql-contrib
		3. sudo su - postgres
		4. psql
		5. CREATE USER catalog WITH PASSWORD 'grader';
		6. ALTER USER catalog CREATEDB;
		7. CREATE DATABASE catalog WITH OWNER catalog;
		8. \c catalog
		9. REVOKE ALL ON SCHEMA public FROM public;
		10. GRANT ALL ON SCHEMA public TO catalog;
		11. \q
		12. exit
		13. Update the database connection in __init__.py, database_setup.py and alotsofinvestment.py to:

			engine = create_engine('postgresql://catalog:grader@localhost/catalog')

		14. Setup the database with: sudo python /var/www/catalog/catalog/database_setup.py
		15. Import the initial data with: sudo python /var/www/catalog/catalog/alotsofinvestment.py

## Step 13. Update Google OAuth Authorized Javascript origins and redirect URL
		1. Get the host name from http://www.hcidata.info/host2ip.cgi
		2. sudo nano /etc/apache2/sites-available/catalog.conf and paste and following below ServerAdmin
		ServerAlias HOSTNAME, i.e. ec2-52-220-149-210.ap-southeast-1.compute.amazonaws.com
		3. Sudo a2ensite catalog
		4. Update IP address and URL in Google Developer console