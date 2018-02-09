# RATIONALE

This repository (desafioluizalabs) implements the challenge issued by Magazine Luiza's Techonology Lab.
The challenge consists of implementing a CRUD application for employee management.
The application was implemented in Python and Django, and provides a RESTful API for employee access, and an admin app (standard Django admin).
I have remarked, at the end of this document, ways to improve and complement the application.

# SETUP:

1. Setup a virtualenv with python 3.6 or greater
2. Install the project dependencies
3. `pip install -r requirements.txt`
4. Fill the local database (SQLite) with fake data, for testing
5. `python manage.py populate_fake_data`
6. Run the django local server
7. `python manage.py runserver 8000`

# USAGE:

## API
1. Request an JWT token:
```
curl -X POST -d "email=admin@admin.com&password=testing12345" http://localhost:8000/api-token-auth/
```
NOTE: by default the `populate_fake_data` command will create an superuser with email: `admin@admin.com` and password: `testing12345`

2. Call any of the endpoints, passing the received token as auth in a header.
```
curl -H "Authorization: JWT <your_token>" http://localhost:8000/departments/
```

## ADMIN

1. Log into Django admin
```
http://localhost:8000/admin
```

NOTE: Endpoint documentation is available under docs/.

# API DOCUMENTATION

API Documentation for this project is available in two forms:

* The Django REST Framework Browseable API

Go to `http://localhost:8000/api` and login at the top right corner.

* API Blueprint doc.

The API Blueprint is a format for specifying APIs, available as a superset of markdown. Any markdown rendered should be able to read the doc, but for best results use the NPM package `aglio`.

A pre-rendered is also available as HTML.

# CODING, FRAMEWORK AND STYLE NOTES:

* I have configured my editor's PEP to a line width of 150 (vs the default 80).
* Python 3.6 and Django 2.0 were chosen, as they are the most up-to-date releases.
* Django-REST-Framework was chosen as the API lib.
* djangorestframework-jwt was chosen as the JWT extension to DRF.
* django-filters was chosen to allow filtering of the endpoints.
* API Blueprint was chosen as the documentation format for API.


# AUTH AND USER MODEL:

* The user model chosen for the application is actually Employee. The chosen approach was to subclass AbstractBaseUser, making an Employee login-able. This might not be the best option for an already existing system/ecosystem. The better option would be to have a dedicated auth/user management micro-service, independent of employee_manager, and integrate them, preferably via a common bus, such as HTTP or even pure TCP and some sort of RPC/IPC.
* The chosen authentication model for the REST API was JWT (JSON Web Token), which has proved very reliable, secure and easy to use compared to other token-auth models.
* NOTE: JWT and other token auth systems are only guaranteed to be secure over TLS/SSL. If you use it on HTTP, you risk beign vulnerable to sniff attacks and man-in-the-middle attacks.

# FIXTURE (FAKE DATA) GENERATION

A simple random approach was used for data generation.
Department names follow the formula `f'Department of {adjective} {substantive}'`, such that `{adjective}` and `{substantive}`
are chosen at random from a small list of words.
Phone numbers are just random digits, and Employee names use the `names` library to acquire random, yet realistic names.

# RUNNING THE TEST SUITE
```
python manage.py test
```

# IMPROVEMENTS (NOT IMPLEMENTED IN THIS POC)

* Pagination of API results
* Never return sequential PKs to client. Use a UUID or other random-generated alphanumeric string as main identifier.
* Improve Admin usability. The implemented ModelAdmins are the most basic available. One should customize its admin interface, depending on business requirements. More properties of ModelAdmin should be used, and html should be overrided, if needed.
* Expand test suite to cover more corner cases and authentication.
* Cache common results, and signal for expiry, as needed.
* Create a Makefile for automatic docs generation, and automatic test running.
* Create a Dockerfile and integrate Docker for build reproducibility and dev ease of use.

