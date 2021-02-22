FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y cron git build-essential python3 texlive-xetex biber texlive-fonts-extra 

COPY . /cv
WORKDIR /cv

COPY build-cron /etc/cron.d/build-cron

RUN chmod 0644 /etc/cron.d/build-cron
RUN chmod +x /cv/dist.sh

RUN crontab /etc/cron.d/build-cron

CMD cron -f