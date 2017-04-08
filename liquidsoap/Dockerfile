# Audio Source server dockerfile.

# Starting from lighter debian distro image (may be optimized --> think about an "from alpine" dockerfile)
FROM debian:wheezy-slim

# Installing liquidsoap and all its plugin to handle multiple audio file formats
RUN apt-get update -y && \
	apt-get install -y liquidsoap liquidsoap-plugin-faad liquidsoap-plugin-flac \
	liquidsoap-plugin-icecast liquidsoap-plugin-lame liquidsoap-plugin-mad liquidsoap-plugin-ogg \
	liquidsoap-plugin-pulseaudio liquidsoap-plugin-samplerate liquidsoap-plugin-taglib \
	liquidsoap-plugin-voaacenc liquidsoap-plugin-vorbis liquidsoap-plugin-xmlplaylist

# Creating a workspace and a user with restricted shell
RUN useradd -m -s /usr/bin/liquidsoap liquy && \
	mkdir -p /home/liquy/audio
WORKDIR /home/liquy

# Copying the main liquidsoap script, conf, and few audio test files.
COPY ./test /home/liquy/var
COPY ./conf.liq /home/liquy/conf.liq
COPY ./fail.mp3 /home/liquy/fail.mp3
COPY ./test.mp3 /home/liquy/test.mp3
COPY ./script.liq /home/liquy/script.liq

# Running Container as restricted shell user
USER liquy

# The entrypoint of this container is a regular liquidsoap script run on foreground. while the source is up, the script keeps going, so as the container
CMD ["./script.liq"]
