# Audio Source server dockerfile.

# Starting from lighter debian distro image (may be optimized --> think about an "from alpine" dockerfile)
FROM debian:wheezy-slim

# Setting env for conf
ENV STREAM_HOST="stream-test.bretzel"
ENV STREAM_PORT=8000
ENV STREAM_SOURCE_PASSWD="sourcepass"
ENV STREAM_MOUNTPOINT="test"
ENV API_HOST="api.bretzel:1337"
ENV SOURCE_ID=1
ENV SOURCE_TOKEN="00000000000000000000000000000000"
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
RUN useradd -m -s /usr/bin/liquidsoap source && \
	mkdir -p /home/source/audio
WORKDIR /home/source

# Copying the main liquidsoap script and audio fail file.
COPY conf/source/fail.mp3 /home/source/fail.mp3
COPY conf/source/script.liq /home/source/script.liq

# Running Container as restricted shell user
WORKDIR /home/source
USER source
# The entrypoint of this container is a regular liquidsoap script run on foreground. while the source is up, the script keeps going, so as the container
ENTRYPOINT ["./script.liq"]
