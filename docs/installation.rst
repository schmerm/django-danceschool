Installation
============

Basic Installation Process
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create a subfolder for your new Django project, and enter it:

   ::

       mkdir django
       cd django

2. Create a new virtual environment and enter it:

   ::

       python3 -m virtualenv .
       source bin/activate

   -  *Note:* Depending on your system, you may need to follow slightly
      modified instructions in order to create a virtual environment. No
      matter which method you use, be sure that your environment is set
      to use Python 3 by default.

3. Install the django-danceschool from `PyPi <https://pypi.python.org/pypi>`_.
   This will also install all of the necessary dependencies (which may take
   awhile)

   ``pip install django-danceschool``

   *Note:* Additionally, depending on your operating system, you may
   need to install certain program dependencies in order to install the
   Pillow package and the psycopg2 package (as listed in
   requirements.txt). If you run into issues at this step of the
   installation, look for these issues first.

4. Start your Django project, using the ``django-admin`` command.  To avoid
   having to set a large number of settings manually, we strongly recommend
   that you use the preexisting installation template as follows.  Make sure
   that you are in the folder where you would like your project to be located when you do this.

   ::

      django-admin startproject --template https://raw.githubusercontent.com/django-danceschool/django-danceschool/master/setup/default_setup.zip <your_project_name>

5. Perform initial database migrations

   ::

       cd <your_project_name> 
       python manage.py migrate

6. Create a superuser so that you can log into the admin interface (you
   will be prompted for username and password)

   ::

       python manage.py createsuperuser

7. **Optional, but strongly recommended:** Run the easy-installer setup
   script, and follow all prompts.  This script will guide you through
   the process of setting initial values for many things, creating a few
   initial pages that many school use, and setting up user groups and
   permissions that will make it easier for you to get started running
   your dance school right away.

   ::

       python manage.py setupschool

8. Run the server and try to log in!

   ::

       python manage.py runserver


Settings Customization and Production Deployment
------------------------------------------------

After performing steps 1-8 above, you should have a working instance of
the danceschool project. However, in order to make the site usable for
your purposes, you will, at a minimum, need to do some basic setting of
settings and preferences

There are two types of settings in this project:

1. Hard-coded settings needed to run the project at all (located in
   settings.py)
2. Runtime settings that customize the site's functionality (stored in
   the database using the 
   `django-dynamic-preferences <http://django-dynamic-preferences.readthedocs.io/en/latest/>`_
   app, and then cached)

If you have used the default setup provided in step 4 above, then you have
already been provided with appropriate default settings for a development
instance of the project. For example, Django's debug mode is on, and the
project uses a SQLite backend to store data instead of a production database
such as PostgreSQL.  Before thoroughly testing out the project, the only
settings that you are required so set in ``settings.py`` are for features
such as email and the Paypal/Stripe integration, because these features
cannot be enabled by default until you have entered credentials for those
services. However, before you deploy this project for "production" purposes,
you will need, *at a minimum*, to customize settings for Paypal/Stripe, email,
and a production-appropriate database.  Also, often time, if your workflow involves
both a development installation and a production installation, there
will be different settings required for each installation.

Here is a list of settings that typically need to be customized in
``settings.py`` before running:

**Django email settings (needed for confirmation emails, etc.)**

- host: ``EMAIL_HOST``
- port: ``EMAIL_PORT``
- username: ``EMAIL_HOST_USER``
- password: ``EMAIL_HOST_PASSWORD``
- use_tls: ``EMAIL_USE_TLS``
- use_ssl: ``EMAIL_USE_SSL``
  
**Django database settings (recommended to change from default SQLite)**:

- ``DATABASES['default']['ENGINE']``
- ``DATABASES['default']['NAME']``
- ``DATABASES['default']['USER']``
- ``DATABASES['default']['PASSWORD']``
- ``DATABASES['default']['HOST']``
- ``DATABASES['default']['PORT']``

** Payment processors **

These are just the settings listed above in :ref:`paypal_setup` and :ref:`stripe_setup`.

For Paypal:

- ``PAYPAL_MODE`` (either "sandbox" or "live")
- ``PAYPAL_CLIENT_ID``
- ``PAYPAL_CLIENT_SECRET``

For Stripe:
- ``STRIPE_PUBLIC_KEY``
- ``STRIPE_PRIVATE_KEY``

For Square:
- ``SQUARE_LOCATION_ID``
- ``SQUARE_APPLICATION_ID``
- ``SQUARE_ACCESS_TOKEN``


Customizing runtime settings is even easier. Simply log in as the
superuser account that you previously created, and go to
http://yoursite/settings/global/. There, you will see organized pages in
which you can change runtime settings associated with various functions
of the site.  If you have run the ``setupschool`` command as instructed
in step 7 above, you will find that sensible defaults for all of the most
important runtime settings have already been put into place for you.

Email Settings
--------------

In order for your project to send emails, you need to specify an SMTP
server that will allow you to send those emails, as well as any
credentials needed to log into that server. These settings are contained
in ``settings.py``. Look for settings such as ``EMAIL_HOST``,
``EMAIL_HOST_USER``, ``EMAIL_HOST_PASSWORD``, etc. to modify them.

Until you set these email settings, you should expect that signing up
new users will return an error, because the app that handles sending
confirmation emails to new users will fail to connect to an email server.

For more details, see the `Django
documentation <https://docs.djangoproject.com/en/dev/topics/email/>`_.

Additionally, because most emails in this project are sent asynchronously,
you will need to run Huey as described below.  If Huey is not running, then
these tasks will be silently queued until Huey is later run.


.. _huey_setup:

Huey (and Redis) setup for production
-------------------------------------

Certain website tasks are best run asynchronously.  For example, when
a student successfully registers for a class, the website does not
need to wait for the confirmation email to be sent in order for the
process to proceed.  Similarly, other tasks such as closing of class
registration are run at regular intervals and do not depend on user
interaction.  For these reasons, this project uses
the `Huey <https://github.com/coleifer/huey>`_ task queue.  Huey is run as
a separate process from your webserver, and when tasks are submitted
to Huey via functions in each app's ``tasks.py``, they are handled by
this separate process.

If you followed the quick start instructions, then Huey is already installed
and a default setup is enabled that will enable you to get going quickly.
On a separate command line from your test server, simply type in 
``python manage.py run_huey`` to run a Huey instance that will handle
sending emails, etc., automatically.  Your site will continue to these
features as well as recurring tasks for as long as this process continues
to run.  

The default settings for Huey involve storing the task queue data in
SQLite-based file storage.  Upon running Huey, you will see a newly
created SQLite file in the same directory as your project's
manage.py file, which stores the task queue data.  Although this approach
allows for convenient setup for testing purposes using the project's
default settings, it is not recommended to use Huey's SQLite storage backend for
production purposes.  Instead, it is strongly recommended that you set up
the popular `Redis <https://redis.io/>`_ cache server, and modify your
``settings.py`` file to use Huey's Redis integration.

Note that These instructions are designed for Linux, and they assume that
you will be running Redis locally using default settings. Getting Redis
running on Windows may require a slightly different process, and
configuring Huey to use a remote Redis installation will also involve
modifying site settings.

1.  Install the Redis client for Python: ``pip install redis``
2.  Start the Redis server: ``sudo service redis-server start``
3.  Add the following to ``settings.py`` (this basic setup can be customized,
    see the `Huey documentation <https://huey.readthedocs.io/en/latest/contrib.html#django>`_).

   ::

      from huey import RedisHuey
      from redis import ConnectionPool
      pool = ConnectionPool(host='localhost', port=6379, max_connections=20)
      HUEY = RedisHuey('danceschool',connection_pool=pool)

4.  As before, run Huey in its own command shell: `python manage.py run_huey`

With these two steps, your installation should now be able to send
emails programmatically, and your site should also run recurring tasks
as long as both Redis and Huey continue to run.

Production deployment of your Django project and of Huey is beyond the scope
of this documentation.  However, solutions such as
`Supervisord <http://supervisord.org/>`_ are generally a preferred approach
to creating a persistent process.

.. _paypal_setup:

Paypal Settings (if using Paypal)
---------------------------------

In order to accept and process Paypal payments, you will need to set up
the credentials for your Paypal account.  As of version 0.1.0 of this
repository, the Django danceschool project uses the
`Paypal REST SDK <https://github.com/paypal/PayPal-Python-SDK>`_.  Older
versions of this repository used the Paypal IPN system, but this
software is no longer maintained, and it is highly recommended that you
upgrade to using the REST API.

REST API Setup
~~~~~~~~~~~~~~

1. Enter your ``settings.py`` file and ensure that the app
   ``danceschool.payments.paypal`` is listed in ``INSTALLED_APPS``.
3. Go to the `Paypal developer website <https://developer.paypal.com/>`_
   and log in using the Paypal account at which you wish to accept
   payments.
4. On the dashboard, under "My Apps & Credentials", find the heading
   for "REST API apps" and click "Create App."  Follow the instructions
   to create an app with a set of API credentials
5. Once you have created an app, you will see credentials listed.  At
   the top of the page, you will see a toggle between "Sandbox" and
   "Live."  If you are setting up this installation for testing only,
   then choose "sandbox" credentials so that you can test transactions
   without using actual money.  For your public installation, use
   "live" credentials.
6. Edit ``settings.py`` to add:
    -  ``PAYPAL_MODE``: Either "sandbox" or "live"
    -  ``PAYPAL_CLIENT_ID``: The value of "Client ID"
    -  ``PAYPAL_CLIENT_SECRET``: The value of "Secret".  **Do not share
    this value with anyone, or store it anywhere that could be publicly
    accessed**


Adding a Paypal "Pay Now" button to the registration page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because this project is designed to be configurable and to accept
different payment providers, the "Pay Now" button is not included by
default on the registration summary page (the last step of the
registration process).  If you have setup your installation by running
the "setupschool" script, and if the ``danceschool.payments.paypal``
app was listed in ``INSTALLED_APPS`` at the time you did so,
then a "Pay Now" button will already be in place.

However, if you have not used the setupschool script, or if you
wish to enable another payment processor after initial setup, then
adding a "Pay Now" button is very straightforward. Follow the steps
for one of these two methods:

Method 1: The Command Line Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Go to the command line in your project's environment and type in
   ``python manage.py setup_paypal``.  The setup script will check
   that your configuration variables allow you to connect to
   Paypal, and you will be prompted with the option to add the button
   plugin to the registration summary page.  If the button is
   already present, then it will not add a duplicate.

Method 2: The CMS method
^^^^^^^^^^^^^^^^^^^^^^^^

1. Log in as a user with appropriate permissions to edit pages and other
   CMS content (the superuser is fine)
2. Proceed through the first two pages of the registration process.
   Entering fake information is fine, as you will not be completing this
   registration.
3. When you get to the registration summary page, click the button in
   the toolbar labeled "Edit Page," then choose "Structure" mode to edit
   the layout of the page.
4. You will see a placeholder for the payment button, called
   "Registration\_Payment\_Placeholder". Click the plus sign (+) next to
   this placeholder to add a plugin, and from the "Paypal" section of
   plugins choose "Paypal Pay Now Form"
5. Configure the plugin (choose which pages to send customers to when
   they have completed/cancelled payment), and you're all set!

To add a gift certificate form to allow customers to purchase gift
certficates, follow a similar procedure, adding the "Paypal Gift
Certificate Form" plugin to any page of your choosing.

.. _stripe_setup:

Stripe Settings (if using Stripe)
---------------------------------

By default, the Django danceschool project now offers the ability to
use the popular Stripe payment processor in place of Paypal.  As with
Paypal, Stripe integration makes use of a modern API that does not
require you to store any sensitive financial information on your own
server, and it requires only that you enable the app and place your
API keys in your ``settings.py`` file.

Stripe API Setup
~~~~~~~~~~~~~~~~

1. Enter your ``settings.py`` file and ensure that the app
   ``danceschool.payments.stripe`` is listed in ``INSTALLED_APPS``.
2.  Go to `Stripe.com <https://www.stripe.com/>`_ and log into your
    account, or sign up for a new account (**Note:** Before running
    transactions in live mode, you will need to activate your account,
    which may involve providing a Tax ID, etc.)
3.  In the dashboard on the left hand side, select "API" to get access
    to your API keys.
4.  You will see test credentials, and if your account has been activated,
    you will also see live credentials.  Enter the following settings into
    your ``settings.py`` file:
   -  ``STRIPE_PUBLIC_KEY``: Your publishable key.
   -  ``STRIPE_PRIVATE_KEY``: Your secret key.  **Do not share
    this value with anyone, or store it anywhere that could be publicly
    accessed**

Adding a Stripe "Checkout Now" button to the registration page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because this project is designed to be configurable and to accept
different payment providers, the "Checkout Now" button is not included by
default on the registration summary page (the last step of the
registration process).  If you have setup your installation by running
the "setupschool" script, and if ``danceschool.payments.stripe`` was listed
in ``INSTALLED_APPS`` at the time you did so, then a "Checkout Now" button 
may already be in place.

However, if you have not used the setupschool script, or if you
wish to enable another payment processor after initial setup, then
adding a "Checkout Now" button is very straightforward. Follow the steps
for one of these two methods:

Method 1: The Command Line Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Go to the command line in your project's environment and type in
   ``python manage.py setup_stripe``.  The setup script will check
   that your configuration variables allow you to connect to
   Stripe, and you will be prompted with the option to add the button
   placeholder on the registration summary page.  If the button is
   already present, then it will not add a duplicate.

Method 2: The CMS method
^^^^^^^^^^^^^^^^^^^^^^^^

1. Log in as a user with appropriate permissions to edit pages and other
   CMS content (the superuser is fine)
2. Proceed through the first two pages of the registration process.
   Entering fake information is fine, as you will not be completing this
   registration.
3. When you get to the registration summary page, click the button in
   the toolbar labeled "Edit Page," then choose "Structure" mode to edit
   the layout of the page.
4. You will see a placeholder for the payment button, called
   "Registration\_Payment\_Placeholder". Click the plus sign (+) next to
   this placeholder to add a plugin, and from the "Stripe" section of
   plugins choose "Stripe Checkout Form"
5. Configure the plugin (choose which pages to send customers to when
   they have completed/cancelled payment), and you're all set!

To add a gift certificate form to allow customers to purchase gift
certficates, follow a similar procedure, adding the "Stripe Gift
Certificate Form" plugin to any page of your choosing.

.. _square_setup:

Square Settings (if using Square)
---------------------------------

As of version 0.4.0 of this project, you are now able to use the
popular Square payment processor in place of either Paypal or Stripe.
In addition to a standard online checkout option that is similar to
Paypal or Stripe, Square *also* allows for easy setup of point-of-sale
payments that can be seamlessly integrated with the Django Dance School
system, by allowing your registration person to click a button that sends
them into the Android or iOS point of sale app, with all details loaded,
and by then reporting the results of your transaction back
to your website at a special "callback" URL.  As with the other payment
processors, Square's modern API means that you are not responsible for
the storage of any sensitive financial information.  For these reasons,
Square is a particularly attractive payment option for schools who need
to take payments at the door.

Please note that this project uses version 2 of the Square Connect
APIs.  As of September 2017, this API is only available in certain countries.
Please see 
`the Square documentation <https://docs.connect.squareup.com/articles/faq-international-availability>`_
for more details.

Additionally, please note that both* the Square point-of-sale integration
and the Square checkout form require that you have HTTPS enabled on your site.
For the checkout form, any page on which the checkout form shows up must be
accessed by HTTPS, or the checkout form will not display.  The checkout form
*will* work on a local test server without HTTPS for testing purposes only.
Setting up HTTPS for your web server is beyond the scope of this documentation,
and the details of its setup will depend on your server configuration.

Square API Setup
~~~~~~~~~~~~~~~~

1. Enter your ``settings.py`` file and ensure that the app
   ``danceschool.payments.square`` is listed in ``INSTALLED_APPS``.
2.  Go to `Squarup.com <https://www.squareup.com/>`_ and log into your
    account, or sign up for a new account.  Go to the "Dashboard".
3.  In the dashboard on the left hand side, select "Apps," then select
    the tab for "My Apps", and click to define a new set of app credentials
    that will be used for your website.
4.  From the "My Apps" page, click on "Manage App", and you will see
    the credentials that you need.  Enter the following settings into
    your ``settings.py`` file.  If you are only seeking to test online
    payments, then you may opt to use the Sandbox credentials (however,
    be advised that Sandbox credentials cannot be used to test point-of-sale
    payments at this time):
   -  ``SQUARE_APPLICATION_ID``: Your application identifier.
   -  ``SQUARE_ACCESS_TOKEN``: Your personal access token.  **Do not share
    this value with anyone, or store it anywhere that could be publicly
    accessed**
   - ``SQUARE_LOCATION_ID``: The first listed value of Location ID listed
    under "Locations."  Please note that the Danceschool project currently
    does not permit distinguishing among multiple locations in the Square
    payment system.
5.  **If you intend to use point of sale integration**, you will also need
    to specify a "callback URL," which is the URL that Square's point of sale
    app sends the details of your transaction to after you successfully complete
    it using their app.  To set this URL, from the "Manage App" page on which you
    accessed your API credentials, click on the "Point of Sale API" tab at the top
    of the page.  Then, under "Web," look for an input labeled "Web Callback URLs."
    In this box, enter your callback URL.  If you are using the default URL
    configuration, this URL will be ``https://yourdomain.com/square/process_pointofsale/``.
    However, you can also check to get the exact URL by running ``python manage.py setup_square``
    from the command line of your project's environment.

Adding a Square Checkout form and/or point of sale button to the registration page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because this project is designed to be configurable and to accept
different payment providers, Square's checkout form and its point-of-sale button are
not included by default on the registration summary page (the last step of the
registration process).  If you have setup your installation by running
the "setupschool" script, and if ``danceschool.payments.square`` was listed
in ``INSTALLED_APPS`` at the time you did so, then a checkout form and/or point of sale button
may already be in place.

However, if you have not used the setupschool script, or if you
wish to enable another payment processor after initial setup, then
adding the form and button are very straightforward. Follow the steps
for one of these two methods:

Method 1: The Command Line Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Go to the command line in your project's environment and type in
   ``python manage.py setup_square``.  The setup script will check
   that your configuration variables allow you to connect to
   Square, and you will be prompted with the option to add the checkout form
   plugin and the point of sale button plugin on the registration summary
   page.  If these plugins are already present, then it will not add duplicates.

Method 2: The CMS method
^^^^^^^^^^^^^^^^^^^^^^^^

1. Log in as a user with appropriate permissions to edit pages and other
   CMS content (the superuser is fine)
2. Proceed through the first two pages of the registration process.
   Entering fake information is fine, as you will not be completing this
   registration.
3. When you get to the registration summary page, click the button in
   the toolbar labeled "Edit Page," then choose "Structure" mode to edit
   the layout of the page.
4. You will see a placeholder for the payment button, called
   "Registration\_Payment\_Placeholder". Click the plus sign (+) next to
   this placeholder to add a plugin, and from the "Square" section of
   plugins, choose the plugin that you desire.
5. Configure the plugin (choose which pages to send customers to when
   they have completed/cancelled payment), and you're all set!

User Permissions for Stripe Point of Sale Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unlike with online payment solutions, with point of sale payment, you
do not want most users to see the point of sale button, and you likely
only want it to show up in circumstances where you will be accepting
this type of payment (i.e. at the door).  So, the following restrictions
are in place:

- Only users with the ``square.handle_pos_payments`` permission set can
  see the point of sale button.  Since superusers have all permissions by
  default, you will see the button if you are logged into a superuser account.
  No other users see the button by default, so it is strongly recommended that
  give this permission to the specific Users who run your registration by going to
  *Apps > Users* on the CMS toolbar.
- Only at-the-door registrations (marked as such during step 1 of the registration process)
  see the button, regardless of who the user is that is performing the registration.
- For transactions that take place on a platform other than Android or iOS,
  the point of sale button will display, but it will be disabled and greyed out,
  to reflect the fact that Square point of sale integration only works on Android
  or iOS platforms.


.. _manual_project_setup:

Manual Project Setup Guide
--------------------------

In setting up your project, it is strongly recommended that you deploy
your new project by running the following:

   ::

      django-admin startproject --template http://leetucker.net/django-danceschool/danceschool_default_setup.zip <your_project_name>

However, it is also possible to deploy a new project by manually
editing ``settings.py`` to enter the needed values.  This section describes
how to do this.

Importing Third-Party Settings
^^^^^^^^^^^^^^^^^

Setting up the Django-danceschool project requires setting a large number of configuration options for third-party apps.  However, these options can be imported automatically so that you do not need to enter them yourself.  Near the top of the ``settings.py`` file, add the following:

   ::

      from danceschool.default_settings import *

Note also that any of the options specified in ``danceschool.default_settings`` can readily be overridden in ``settings.py``.  Just be sure to set your chosen setting values *below* the import command above.

Installed Apps
^^^^^^^^^^^^^^

In addition to the various apps that are components of the danceschool project, there are several other apps that need to be added to your project's ``INSTALLED_APPS``.  It is important to note that the order in which apps are added often matters.  In particular, because Django's template loading and URL pattern matching functions use the first matching template/pattern, some apps need to be loaded before others in order for them to function correctly.

First, list the Django CMS app in ``INSTALLED_APPS``, followed by the Django dynamic preferences app.  These apps go first so that they can find and register CMS plugins and dynamic preferences from other apps:

   ::
      'cms',
      'dynamic_preferences',

Next, list the core danceschool app, which provides all of the necessary functionality of the project, and is required.  If you have setup any custom app which overrides the templates used by the danceschool project, then this should also be listed here:

   ::
      # '<your_custom_app>',
      'danceschool.core',

The ``danceschool.core`` app contains all of the necessary basic functionality of the project.  However, depending on your needs, you may want to install some of all of the following apps by adding them to ``INSTALLED_APPS``:

   ::

      'danceschool.financial',        # Financial reporting and expense/revenue tracking
      'danceschool.private_events',   # Non-public events and calendar with reminders and feeds
      'danceschool.discounts',        # Configurable registration discounts
      'danceschool.vouchers',         # Vouchers, gift certificates, and the referral program
      'danceschool.prerequisites',    # Configurable prerequisites for specific classes
      'danceschool.stats',            # School performance statistics
      'danceschool.news',             # A simple news feed
      'danceschool.faq',              # A simple FAQ system
      'danceschool.payments.paypal',  # Paypal Express Checkout payment processor
      'danceschool.payments.stripe',  # Stripe Checkout payment processor

Then, before including the Django contrib apps, add the following apps (the order of these does not matter, but some apps *must* be listed before ``django.contrib.admin``):

   ::

      'adminsortable2',
      'allauth',
      'allauth.account',
      'allauth.socialaccount',
      'ckeditor_filebrowser_filer',
      'crispy_forms',
      'dal',
      'dal_select2',
      'daterange_filter',
      'djangocms_admin_style',
      'djangocms_forms',
      'djangocms_text_ckeditor',
      'easy_pdf',
      'easy_thumbnails',
      'filer',
      'huey.contrib.djhuey',
      'menus',
      'polymorphic',
      'sekizai',
      'treebeard',

Finally, be sure that the following django contrib apps are all listed in ``INSTALLED_APPS`` at the bottom:

   ::

      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'django.contrib.sites',
      'django.contrib.sitemaps',
      'django.contrib.admin',


Template settings
^^^^^^^^^^^^^^^^^
Django CMS requires some specialized context processors to be enabled.  So, add the following to ``TEMPLATES['OPTIONS']['context_processors']``:

   ::

      'cms.context_processors.cms_settings',
      'sekizai.context_processors.sekizai',

Middleware
^^^^^^^^^^

Django CMS requires the following to be added to ``MIDDLEWARE_CLASSES``:

At the top:

   ::

      'cms.middleware.utils.ApphookReloadMiddleware',

Anywhere in MIDDLEWARE_CLASSES:
  
   ::

      'django.middleware.locale.LocaleMiddleware',
      'cms.middleware.user.CurrentUserMiddleware',
      'cms.middleware.page.CurrentPageMiddleware',
      'cms.middleware.toolbar.ToolbarMiddleware',
      'cms.middleware.language.LanguageCookieMiddleware',

Site ID and Language Code
^^^^^^^^^^^^^^^^^^^^^^^^^

Because Django CMS makes use of ``django.contrib.sites``, in order
for a default URL to be available for pages, the CMS needs to know
the database identifier ofyour default site.  For most installations,
this means adding:

   ::

      SITE_ID = 1

Django CMS also uses slightly different language designations than Django
as a whole.  By default, Django's ``settings.py`` ships with
``LANGUAGE_CODE = 'en-us'``.  Assuming that your site will be running in
English, you should change this to ``LANGUAGE_CODE = 'en'``.

URL Handling
^^^^^^^^^^^^

The Danceschool project has a single ``urls.py`` file which handles all
of the URLs for the project and its core dependencies.  Similarly, Django
CMS requires a catch-all URL pattern that tries to match any unmatched
URLs to CMS pages.  So, be sure to add the following code to the bottom
of your ``urls.py``.

   ::

      from django.conf.urls import include, url

      ...


      # Add this at the bottom of urls.py
      urlpatterns += [
          # Include your own app's URLs first to override default app URLs
          # url(r'^', include('<yourapp>.urls')),
          # Now, include default app URLs and CMS URLs
          url(r'^', include('danceschool.urls')),
          url(r'^', include('cms.urls')),
      ]

**Note:** If for any reason you wish to modify any of the default URL paths
provided by the project, you can do so by adding your own URLs prior to the
inclusion of ``danceschool.urls``.

Other Settings You May Wish to Modify
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As with all Django projects, you are generally free to modify other
settings as you see fit.  However, there are certain other settings
that are commonly modified for each installation, and that you will
likely wish to modify.

For more information on these settings, see the 
`Django documentation <https://docs.djangoproject.com/en/dev/ref/settings/>`_.

**Static file storage/upload settings**:

- ``STATIC_URL`` (set to "/static/" by default)
- ``STATIC_ROOT``
- ``MEDIA_ROOT``
- ``MEDIA_URL``
- ``CKEDITOR_UPLOAD_PATH``

**Django email settings (needed for confirmation emails, etc.)**

- host: ``EMAIL_HOST``
- port: ``EMAIL_PORT``
- username: ``EMAIL_HOST_USER``
- password: ``EMAIL_HOST_PASSWORD``
- use_tls: ``EMAIL_USE_TLS``
- use_ssl: ``EMAIL_USE_SSL``
  
**Django database settings (recommended to change from default SQLite)**:

- ``DATABASES['default']['ENGINE']``
- ``DATABASES['default']['NAME']``
- ``DATABASES['default']['USER']``
- ``DATABASES['default']['PASSWORD']``
- ``DATABASES['default']['HOST']``
- ``DATABASES['default']['PORT']``

**Django-filer settings**

See the `Django-filer documentation <https://django-filer.readthedocs.io/en/latest/installation.html>`_
for more details:

- ``FILER_STORAGES``
- ``DEFAULT_FILER_SERVERS``
  
** Payment processors **

These are just the settings listed above in :ref:`paypal_setup` and :ref:`stripe_setup`.

For Paypal:

- ``PAYPAL_MODE`` (either "sandbox" or "live")
- ``PAYPAL_CLIENT_ID``
- ``PAYPAL_CLIENT_SECRET``

For Stripe:
- ``STRIPE_PUBLIC_KEY``
- ``STRIPE_PRIVATE_KEY``
