# Streaming server dockerfile

# Starting from lighter debian distro image (may be optimized --> think about an "from alpine" dockerfile)
FROM debian:wheezy-slim

# Installing icecast
RUN apt-get update -y && \
	apt-get install -y icecast2

# Copying icecast conf
COPY conf/stream/test/icecast.xml /etc/icecast2/icecast.mxl

# Run container
USER icecast2
# Overide the start command to load another conf file.
ENTRYPOINT ["icecast2", "-c", "etc/icecast2/icecast.xml"]
