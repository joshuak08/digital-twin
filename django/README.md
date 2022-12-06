# Getting Started with Django

## Index

- [Django Installation](#django)
- [Python Environment](#python)
- [Database and Migrations](#database)

Prerequisites: **Python 3**

## Django

Follow [this](https://docs.djangoproject.com/en/4.1/topics/install/#install-the-django-code) official guide to install
Django:

1. Clone the directory and cd into `django`
1. Make sure pip is installed by running `pip --version`
2. Create a virtual environment **(or just install Django with `python -m pip install Django`)**
3. Run the server by changing directory into the `watertreatment` project and running `python3 manage.py runserver`

## Python

Follow [this](https://docs.python.org/3/tutorial/venv.html) tutorial to start a Python virtual environment.

**Or**

Follow the following guide to set up a virtual environment.

--- 
**Create a virtual environment** by running. x
`python3 -m venv django-env`

> You can name the environment anything you want - I named mine `django-env`.

To activate the virtual environment.

On Windows, **run**:

`django-env\Scripts\activate.bat`

On Unix or MacOS, **run**:

`source django-env/bin/activate`

Install necessary packages with:

`python -m pip install -r requirements.txt`

> Do this in your activated environment. It should show `$ (django-env)` in your shell.

The **venv** and **src** files should be **separate**:

`django-env  README.md  requirements.txt  watertreatment
`

---

To **run the website**, cd into `watertreatment` project and run:

`python3 manage.py runserver`

--- 

To deactivate a virtual environment, type:

`deactivate`

--- 

Don't push your virtual environment to Github. \
You want to [freeze](https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip) your dependencies to a
requirements.txt and push that.

You can do this by running

`python -m pip freeze > requirements.txt`#

## Database

`$ python manage.py makemigrations`

`$ python manage.py migrate`
