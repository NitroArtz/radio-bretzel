# Audio Source server dockerfile.

# Starting from lighter debian distro image (may be optimized --> think about an "from alpine" dockerfile)
FROM debian:wheezy-slim

# Installing liquidsoap and all its plugin to handle multiple audio file formats
RUN apt-get update -y && \
	apt-get install -y liquidsoap liquidsoap-plugin-faad liquidsoap-plugin-flac \
	liquidsoap-plugin-icecast liquidsoap-plugin-lame liquidsoap-plugin-mad liquidsoap-plugin-ogg \
	liquidsoap-plugin-pulseaudio liquidsoap-plugin-samplerate liquidsoap-plugin-taglib \
	liquidsoap-plugin-voaacenc liquidsoap-plugin-vorbis liquidsoap-plugin-xmlplaylist

# Creating a workspace and a user
RUN useradd -m -s /usr/bin/liquidsoap liquy && \
	mkdir -p /home/liquy/audio && \
	mkdir /home/liquy/scripts
WORKDIR /home/liquy

# Copying the main liquidsoap script, conf, and few audio test files.
COPY ./test /home/liquy
COPY ./conf.liq /home/liquy/conf.liq
COPY ./fail.mp3 /home/liquy/fail.mp3
COPY ./script.liq /home/liquy/script.liq

Running Container
USER liquy
CMD ["./script.liq"]
