# Flask-Bootstrap Dockerfile
FROM ubuntu:16.04

MAINTAINER Will Marshall <will.marshall@vertical-knowledge.com>

RUN apt-get update && apt-get install -y nodejs-legacy npm software-properties-common python3-pip python3-psycopg2

ADD ./requirements.txt requirements.txt
RUN pip3 install -r ./requirements.txt

ADD ./Application Application
ADD ./manage.py manage.py
ADD ./uwsgi.ini uwsgi.ini

ENV APP_ENV docker
ENV NODE_ENV production

RUN cd Application/app_src && npm install && node node_modules/webpack/bin/webpack.js

# Don't expose any ports if running with --net=host for
# EXPOSE <ports>
ENTRYPOINT ["./manage.py"]
CMD ["run_uwsgi"]
