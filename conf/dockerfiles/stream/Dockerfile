# Streaming server dockerfile

# Starting from lighter debian distro image (may be optimized --> think about an "from alpine" dockerfile)
FROM debian:wheezy-slim

# Installing icecast
RUN apt-get update -y && \
	apt-get install -y icecast2 && \
	mkdir /etc/icecast2/test && \
	chown -R icecast2:icecast /etc/icecast2/
# Copying icecast conf
COPY conf/stream/test/icecast.xml /etc/icecast2/test/icecast.mxl

# Run container
USER icecast2
# Overide the start command to load another conf file.
ENTRYPOINT ["icecast2", "-c"]
CMD ["/etc/icecast2/test/icecast.xml"]
