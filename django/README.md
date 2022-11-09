# water-twin-env

## Getting Started

Follow [this](https://docs.python.org/3/tutorial/venv.html) tutorial to start a python venv.

Or

---
Create a virtual environment, decide upon a directory (a common place is .venv) where you want it, and run:

`python3 -m venv tutorial-env`

---

To activate the virtual environment.

On Windows, run:

`django-env\Scripts\activate.bat`

On Unix or MacOS, run:

`source django-env/bin/activate`

Install necessary packages with (in your env):

`python -m pip install -r requirements.txt`

---

To **run the website**, cd into `watertreatment` project and run:

`python3 manage.py runserver`

--- 

To deactivate a virtual environment, type:

`deactivate`

--- 

Don't push your env to Github. You want to [freeze](https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip) your dependencies to requirements.txt and push that. 

**TODO**

- Deploy to some host
- Write some tests
- Configure database to store component attributes
- Interface with the Django backend
- CI/CD  

