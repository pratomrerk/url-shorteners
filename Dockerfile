FROM python:3.10-slim

RUN python -m pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip install Flask Flask-Cors redis gunicorn[gevent]
#RUN pip install -r requirements.txt
#RUN pip install gunicorn[gevent]

99=

EXPOSE 7788
#workers = (2*<num_cores>)+1
CMD ["python", "-m", "gunicorn", "--workers", "9", "--bind", "0.0.0.0:7788", "app:app"]