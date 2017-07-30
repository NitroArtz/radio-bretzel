# Trails Dockerfile
FROM node:alpine

MAINTAINER Papy-Bretzel <papybretzel@protonmail.com>

# Creating a workspace for the application
RUN mkdir -p /usr/src/app
# Copying source code
# COPY ../../../api/ /usr/src/app/

# Installing all node modules
WORKDIR /usr/src/app/
# RUN npm install

# Running the container
USER node

ENTRYPOINT ["/usr/local/bin/npm", "start"]
