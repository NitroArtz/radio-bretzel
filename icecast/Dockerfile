# Streaming server dockerfile

# Starting from lighter debian distro image (may be optimized --> think about an "from alpine" dockerfile)
FROM debian:wheezy-slim

# Installing icecast
RUN apt-get update -y && \
	apt-get install -y icecast2

# Copying icecast conf
COPY ./icecast.xml /etc/icecast2/icecast.xml

# Run container
USER icecast2
CMD ["icecast2", "-c", "/etc/icecast2/icecast.xml"]
