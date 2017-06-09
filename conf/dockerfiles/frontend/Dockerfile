# Front-end server dockerfile

# Starting from the lightest image of the official NodeJS project.
FROM node:alpine

# Creating a workspace for the application
RUN mkdir -p /usr/src/app/upload

# Installing all node modules
COPY frontend/server/package.json /usr/src/app/
WORKDIR /usr/src/app
RUN npm install

# Copying application source code
COPY frontend/server/app.js /usr/src/app/
COPY frontend/server/src /usr/src/app/src

# Start the container
USER node
CMD ["node", "app.js"]
