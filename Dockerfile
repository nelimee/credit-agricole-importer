FROM python:3.11-slim-buster

# cron related commands
RUN apt-get update && apt-get -y install cron
COPY ./crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# Python application related commands
WORKDIR /app
COPY ./ /app/
RUN python -m pip install -r requirements.txt

# The main.py execution is done in the crontab
CMD ["crond", "-f", "-L", "/dev/stdout"]
