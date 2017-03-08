FROM debian:wheezy-slim

RUN apt-get update -y && \
	apt-get install -y liquidsoap liquidsoap-plugin-faad liquidsoap-plugin-flac \
	liquidsoap-plugin-icecast liquidsoap-plugin-lame liquidsoap-plugin-mad liquidsoap-plugin-ogg \
	liquidsoap-plugin-pulseaudio liquidsoap-plugin-samplerate liquidsoap-plugin-taglib \
	liquidsoap-plugin-voaacenc liquidsoap-plugin-vorbis liquidsoap-plugin-xmlplaylist

RUN mkdir -p /ls/audio && \
	useradd liquy -d /ls -s /bin/bash && \
	chown -R liquy:liquy /ls

COPY ./ls/audio/fail.mp3 /ls/audio/fail.mp3

COPY ./ls/audio/test/test.mp3 /ls/audio/test.mp3

COPY ./scripts/test.liq /test.liq

COPY ./scripts/runstream /runstream

WORKDIR /

ENTRYPOINT ./runstream
