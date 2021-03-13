FROM python:3.7-stretch

WORKDIR /app

ADD . /app

# install for opencv use
RUN apt update && apt -y upgrade && \
    apt install -y libgl1-mesa-glx

RUN pip install -r requirements.txt

EXPOSE 8888

#CMD python Flask.py
CMD uwsgi --socket :8888 --wsgi-file app.py --callable app --processes 4 --threads 2 --py-autoreload=1