FROM python:3.8

RUN mkdir /code
RUN mkdir /data

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000
COPY ./src /code/
