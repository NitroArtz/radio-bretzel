FROM debian:wheezy-slim

RUN apt-get update -y && \
	apt-get install -y liquidsoap liquidsoap-plugin-faad liquidsoap-plugin-flac \
	liquidsoap-plugin-icecast liquidsoap-plugin-lame liquidsoap-plugin-mad liquidsoap-plugin-ogg \
	liquidsoap-plugin-pulseaudio liquidsoap-plugin-samplerate liquidsoap-plugin-taglib \
	liquidsoap-plugin-voaacenc liquidsoap-plugin-vorbis liquidsoap-plugin-xmlplaylist

RUN useradd -m -s /usr/bin/liquidsoap liquy && \
	mkdir /home/liquy/audio && \
	mkdir /home/liquy/scripts

WORKDIR /home/liquy

COPY ./audio /home/liquy/audio

COPY ./scripts /home/liquy/scripts

COPY ./runstream /home/liquy/runstream

USER liquy

ENTRYPOINT ./scripts/test.liq
