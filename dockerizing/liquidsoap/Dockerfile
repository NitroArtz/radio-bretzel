FROM debian:wheezy-slim

RUN apt-get update -y && \
	apt-get install -y liquidsoap liquidsoap-plugin-faad liquidsoap-plugin-flac \
	liquidsoap-plugin-icecast liquidsoap-plugin-lame liquidsoap-plugin-mad liquidsoap-plugin-ogg \
	liquidsoap-plugin-pulseaudio liquidsoap-plugin-samplerate liquidsoap-plugin-taglib \
	liquidsoap-plugin-voaacenc liquidsoap-plugin-vorbis liquidsoap-plugin-xmlplaylist

RUN mkdir /audio

COPY ./audio/fail.mp3 /audio/fail.mp3

COPY ./audio/test/test.mp3 /audio/test.mp3

COPY ./scripts/test.liq /test.liq

ENTRYPOINT /test.liq
