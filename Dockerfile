FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV WORKDDIR /app
WORKDIR ${WORKDDIR}
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000
