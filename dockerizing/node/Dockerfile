# Front-end server dockerfile

# Starting from the lightest image of the official NodeJS project.
FROM node:alpine

# Creating a workspace for the application
RUN mkdir -p /usr/src/app/upload
WORKDIR /usr/src/app

# Installing all node modules
COPY ./server/package.json /usr/src/app/
RUN npm install

# Copying application source code
COPY ./server/app.js /usr/src/app/
COPY ./server/src /usr/src/app/src

# Start the container
USER node
CMD ["node", "app.js"]
