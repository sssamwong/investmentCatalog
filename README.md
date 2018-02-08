# Linux Server Configuration

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
		2. git config --global user.name "Sam W"
		3. git config --global user.email siuswong6@gmail.com

## Step 9: Clone the Catalog from Github
		1. cd /var/www
		2. sudo mkdir catalog
		3. sudo chown -R grader:grader catalog
		4. git clone https://github.com/sssamwong/Udacity-FSWD
		5. cd catalog
		6. sudo nano catalog.wsgi

			#!/usr/bin/python
			import sys
			import logging
			logging.basicConfig(stream=sys.stderr)
			sys.path.insert(0,"/var/www/catalog/Udacity-FSWD/Project_Item_Catalog_App/vagrant")

			from FlaskApp import app as application



## Step 8. Install PostgreSQL
		1. sudo apt-get install libpq-dev python-dev
		2. sudo apt-get install postgresql postgresql-contrib
		3. 



This is a website written in python code running on a virtual machine and terminal/command line to an investment catalog with function to add, modify and delete catagories and investments, if authorized and authenicated.

## Software requirement

Code was written in python 2, SQLAlchemy Google Oauth 2.0 for login. While the code is run in the virtual machine and terminal/command line, the below will be required:

  1. Python 2
  2. SQLAlchemy
  3. A Google account
  4. Virtual Machine (Vagrant and VirtualBox)
  5. Terminal or command line

### How to Use

The code should be run from the terminal and command line following the below steps:

  *    Download from the below github directory

  Github [here](https://github.com/sssamwong/Udacity-FSWD/tree/master/Project_Item_Catalog_App/vagrant)

  *  Open Terminal or command line
  *  cd to the directory of the download
  *  Connect to the virtual machine by typing 'vagrant up' and 'vagrant ssh' in the terminal or command line
  *  cd /vagrant
  *  Run the project.py by entering - 'python project.py'
  *  Open Chrome or other browers
  *  Go to http://localhost:8000/
  *  Start to explore

#### JSON API Endpoint

API could be access through below:

  *  http://localhost:8000/json/catalog
  *  http://localhost:8000/json/catalog/<id of the category>

#### Contribution

Any suggestion or recommendation please send an email to siuswong6@gmail.com

#### Credit to investopedia and wikipedia for the initial descriptions