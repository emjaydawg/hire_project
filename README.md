# hire_project
HIRE simplifies and streamlines the job search process for the formerly incarcerated.




# Contributing to this project

## Technical Setup

These are the technical steps needed to clone this repository, and setup your
environment so that you can help contribute to this project.

You will need a version of Python3 installed on your system. The instructions
will help you setup an isolated Python environment for your poject.

## First time setup

1. Get the source code: `git clone https://github.com/emjaydawg/hire_project.git`
2. `cd hire_project`
3. Create virtual enviornment: `python3 -m venv venv`
4. Activate virtual environment: `source venv/bin/activate`
5. Ensure pip is the latest version: `pip install --upgrade pip`
6. Install latest software: `pip pinstall -r requirements.txt`
7. Create a random DJANGO_SECRET_KEY in your login
   For example, add this to your $HOME/.bashrc file: `export DJANGO_SECRET_KEY=develop_secret`


## Whenever you start working

1. `cd hire_project`
2. `source venv/bin/activate` (Your prompt should now have `(venv)` within it
3. Ensure DJANGO_SECRET_KEY environment variable is set
   (`echo $DJANGO_SECRET_KEY` should return something and not be blank)
4. `cd hire`
5. Start the webserver: `./manage.py runserver`
