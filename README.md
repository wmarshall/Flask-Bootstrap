# Flask App Bootstrap
An simple Flask app Template with:
* User Authentication
* Notifications
* Webpack + ES2015 + Bootstrap Frontend
* Asset Management
* Sass Styles

# First Time Setup

```
pip install -r requirements.txt
cd Application/app_src && npm install && node node_modules/webpack/bin/webpack.js
./manage.py db upgrade
./manage.py create_user
```

#Starting the development Server
## Set the environmental variables

```
export APP_ENV="dev"
```
## Start the server
```
./manage.py runserver
```

# Database migrations
```
./manage.py db migrate
./manage.py db upgrade
```

## Production

```
export APP_ENV=prod
export NODE_ENV=production
```

### Docker
```
docker build .
docker run <hash>
docker run <hash> celery_worker
```

### Bare metal
```
./manage.py run_uwsgi
./manage.py celery_worker
```
