# Flask App Bootstrap
An simple Flask app Template with:
* User Authentication
* Module Angular App Layout
* Partial minification
* Asset Management
* Style framework

# Dev Environment Dependencies
* bower-cli
* postgres

# First Time Setup

pip install -r requirements.txt

```
npm install
python manage.py create_db
python manage.py db upgrade
python manage.py create_user
```

#Starting the development Server
### Set the enviormetal variables

```
export APP_ENV="dev"
```
### Start the server
```
python manage.py runserver
```

# Database migrations
```
python manage.py db migrate
python manage.py db upgrade
```