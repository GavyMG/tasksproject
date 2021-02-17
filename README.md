Basic Rest Api for tasks
========================

# Installation (dev)

## Linux
```bash
# Download the folder project
cd tasksproject
# create a new virtual environment for the project
python3 -m venv env
source env/bin/activate
# Install requirement.txt
pip install -r requirement.txt
# prepare the db
python manage.py makemigrations
python manage.py makemigrations tasksapp
python manage.py migrate
# create superuser
python manage.py createsuperuser
# runserver
python manage.py runserver
```

# Usage

PS: New users needs to be created in the admin page (because right now there is not registration option).
