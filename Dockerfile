FROM python:3.10.4-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD requirements.txt .

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

RUN rm requirements.txt