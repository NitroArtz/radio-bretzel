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

# Params about sails-permissions
COPY ./sails-permissions-default-config/admin-user.js:/usr/src/app/node_modules/sails-permissions/config/fixtures/user.js
COPY ./sails-permissions-default-config/permissions.js:/usr/src/app/node_modules/sails-permissions/config/permissions.js

# Running the container
USER node
CMD ["/usr/local/bin/sails", "lift"]
