FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV HOME /app
RUN pwd
WORKDIR ${HOME}
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
