# Sails Backend Dockerfile
FROM node:alpine


# Creating a workspace for the application
RUN mkdir -p /usr/src/app
RUN npm install -g sails

# Copying source code
# COPY ../../../api/ /usr/src/app/
COPY api/package.json /usr/src/app/package.json

# Installing all node modules
WORKDIR /usr/src/app/
RUN npm install

# Params about sails-permissions
COPY api/sails-permissions-default-config/admin-user.js /usr/src/app/node_modules/sails-permissions/config/fixtures/user.js
COPY api/sails-permissions-default-config/permissions.js /usr/src/app/node_modules/sails-permissions/config/permissions.js

# Running the container
USER node
CMD ["/usr/local/bin/sails", "lift"]
