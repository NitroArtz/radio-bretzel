FROM debian:wheezy-slim

RUN apt-get update -y && \
	apt-get install -y liquidsoap liquidsoap-plugin-faad liquidsoap-plugin-flac \
	liquidsoap-plugin-icecast liquidsoap-plugin-lame liquidsoap-plugin-mad liquidsoap-plugin-ogg \
	liquidsoap-plugin-pulseaudio liquidsoap-plugin-samplerate liquidsoap-plugin-taglib \
	liquidsoap-plugin-voaacenc liquidsoap-plugin-vorbis liquidsoap-plugin-xmlplaylist

RUN useradd -m -s /usr/bin/liquidsoap liquy && \
	mkdir -p /home/liquy/audio && \
	mkdir /home/liquy/scripts

WORKDIR /home/liquy

COPY ./test /home/liquy
COPY ./conf.liq /home/liquy/conf.liq
COPY ./fail.mp3 /home/liquy/fail.mp3
COPY ./script.liq /home/liquy/script.liq

USER liquy

ENTRYPOINT ["./script.liq"]
