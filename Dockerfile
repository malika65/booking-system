FROM python:3.9.5

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1

RUN mkdir /app -p && mkdir /app/static -p
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./worker_start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./beat_start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./flower_start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

#COPY . /app/
#RUN chmod +x /app/entrypoint.sh
#ENTRYPOINT ["/app/entrypoint.sh"]