FROM debian:wheezy-slim

RUN apt-get update -y && \
	apt-get install -y icecast2 && \
	chsh -s /bin/bash icecast2

COPY ./config /etc/

COPY ./runIcecast /

ENTRYPOINT /runIcecast
