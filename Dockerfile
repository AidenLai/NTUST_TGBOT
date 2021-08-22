FROM python:3.8
MAINTAINER Aiden

WORKDIR /usr/src/app/TGBot
COPY . .
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
