# Audio Source server dockerfile.

# Starting from lighter debian distro image (may be optimized --> think about an "from alpine" dockerfile)
FROM debian:wheezy-slim

# Setting env for conf
ENV ICECAST_HOST="icecast-test.bretzel"
ENV ICECAST_PORT=8000
ENV ICECAST_SOURCE_PASSWD="sourcepass"
ENV ICECAST_MOUNTPOINT="test"
ENV SOURCE_NAME="Radio Test"
ENV SOURCE_DESC="Bretzel Radio Test"
ENV SOURCE_GENRE="test"

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

# Copying the main liquidsoap script and audio fail file.
COPY ./fail.mp3 /home/liquy/fail.mp3
COPY ./script.liq /home/liquy/script.liq

# Running Container as restricted shell user
USER liquy

# The entrypoint of this container is a regular liquidsoap script run on foreground. while the source is up, the script keeps going, so as the container
CMD ["./script.liq"]
