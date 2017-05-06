# File Server Dockerfile
FROM debian:wheezy-slim

RUN mkdir /srv/audio
RUN useradd -p sourcepass -d /srv/audio -N -s /dev/null source
RUN useradd -p backendpass -d /srv/audio -N  -s /dev/null backend

RUN apt-get update && \
  apt-get -y install vsftpd

COPY ./vsftpd.conf /etc/vsftpd.conf

VOLUME ["/srv/audio"]

CMD ["vsftpd", "/etc/vsftpd.conf"]
