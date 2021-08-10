FROM python:3.9
MAINTAINER Aiden

RUN pip3 install pipenv
WORKDIR /usr/src/app
COPY . .
RUN pipenv --three
RUN pipenv install

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
