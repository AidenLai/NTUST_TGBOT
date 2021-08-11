FROM python:3.8
MAINTAINER Aiden

WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
VOLUME ["usr/scr/app/course/token.txt"]

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
