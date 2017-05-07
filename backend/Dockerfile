# Sails Backend Dockerfile

FROM node:alpine

# Creating a workspace for the application
RUN mkdir -p /usr/src/app
RUN npm install -g sails

# Copying source code
# COPY ./backend/ /usr/src/app/
COPY ./backend/package.json /usr/src/app/package.json

WORKDIR /usr/src/app/

# Installing all node modules
RUN npm install

# Running the container
USER node
CMD ["/usr/local/bin/sails", "lift"]
