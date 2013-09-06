BVD
==========

BVD is a tool for monitoring and presenting the status of CI Builds running on multiple Jenkins installation for Voltage Security.  The software has been made open source under the BSD license.

BVD is exensible in that it does not rely on any particular CI System, and can be used with any CI system of your choosing, by plugging in a module which connects to your desired CI System, and returns the following JSON for each desired CI build to be monitored:

    return dict(
            jobname = jobname,
            status   = status,
        )

The BVD GUI allows you to monitor CI builds by entering the following parameters:

    1) Hostname of CI Server
    2) Name of Build
    3) Display name (Optional).  This is the name that will be displayed on the widget

BVD reports on the various statuses of CI builds via colored widgets with icons representing each state, ex:

    1) A successful last build: Green Widget with Check Mark icon
    2) A failed last build    : Red Widget with X icon
    3) An unstable build      : Yellow Widget with Cloud icon
    4) A down host            : Grey Widget

Insallation Requirements
========================

1) You should install pip (but is not required), which will simplify the installation of required libraries, which can be found in the requirements.txt in the project root directory

2) If you would like an automated install, you will need to install fabric.

3) SqlLite-3 (Required)


Automated Dev Installation
======================

1) Install fabric, via easy_install: ex: 

    $ sudo apt-get install python-distribute #will install easy_install 
    $ sudo easy_install fabric


2) Install pip via via easy_install: ex: 

    $ sudo easy_install pip

3) Navigate to the project root, where the file fabfile.py exists

4) Run the following command (notice: you DO NOT need sudo access): 

    $ fab local

5) Open your browser and point it to: 
    
    http://localhost:8000

Configuring Apache and Setting Up Production
============================================

1) Set your installation directory in the fabfile by editing path_to_bvd at the top of the file. EX:

    path_to_bvd = '/is/actually/over/here'

2) Run

    $ sudo fab configure_apache

3) Add these lines to your httpd.conf:

    LoadModule wsgi_module libexec/apache2/mod_wsgi.so
    Include {{ path_to_bvd}}/src/config/bvd.conf
    
    where {{ path_to_bvd }} is the location of the installation of BVD

4) SSL
    
    If you're using SSL, copy your .crt and .key to src/certs/ and edit src/config/bvd.conf to match
    
    If you're not using SSL, remove the lines regarding SSL from src/config/bvd.conf

5) Restart Apache

    $ sudo apachectl -k restart

6) To Automatically load BVD at login on OS X run

    $ fab configure_automatic_start_on_login_osx

7) [optional] Test that the login script works with

    $ launchctl start com.user.loginscript

8) If you have a database error, make sure that bvd.db is writable by apache.

Automated Installation Explanation
==================================

The automated install script will download and install all required libraries via the folowing command:

    $ pip install --user -r requirements.txt

which will store all required libraries at the user level, and not the system level, thereby not needing sudo access

the script then runs the following command

    $ python manage.py syncdb

which will create the required database and associated database tables, then the installer will run

    $ python manage.py runserver

which starts the django developement server, such that you can view the application for testing purposes



