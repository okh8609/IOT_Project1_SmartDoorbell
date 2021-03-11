FROM python:3.7-stretch

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8888

#CMD python Flask.py
CMD uwsgi --socket :8888 --wsgi-file flask_.py --callable app --processes 4 --threads 2 --py-autoreload=1