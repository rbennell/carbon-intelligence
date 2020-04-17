FROM python:3.8

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY ./src /code

EXPOSE 8000
