FROM debian:wheezy-slim

RUN apt-get update -y && \
	apt-get install -y icecast2 && \
	chsh -s /bin/bash icecast2

COPY ./config /etc/icecast2

USER icecast2

ENTRYPOINT ["icecast2", "-c", "/etc/icecast2/icecast.xml"]
