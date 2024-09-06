How I created the project (commands):
  python -m venv venv
  venv\Scripts\activate
  pip install django
  django-admin startproject taskListDjango .

Start the virtual enviroment if not already started:
  venv\Scripts\activate

Stop the virtual enviroment:
  deactivate

To create a new app inside the project:
  python manage.py startapp myapp

Start The Project:
  python manage.py runserver

The venv folder is git ignored, the dependencies are listed in requirements.txt using:
  pip freeze > requirements.txt

To install dependencies automatically:
  pip install -r requirements.txt

To create superuser (only after creating the migrations in db):
  python manage.py createsuperuser

To make migrations:
  python manage.py makemigrations

To save migrations to database:
  python manage.py migrate

