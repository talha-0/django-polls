# Getting started
Create a new environment for the project.

* Install requirements
```bash
pip install -r requirements.txt
```

* Create a django project
```bash
django-admin startproject <project name>
```

* Or create project in a different directory
```bash
mkdir <dir name>
django-admin startproject <project name> <dir name>
```

* Create an app (Multiple app can be created)
```bash
python manage.py startapp <app name>
```

* Run the server
```bash
python manage.py runserver
```

* Create basic tables
```bash
python manage.py migrate
```

* Create additional tables for app models
First add the add in the setting->installed apps then run the following command:
```bash
python manage.py makemigrations <app name>
python manage.py migrate
```
