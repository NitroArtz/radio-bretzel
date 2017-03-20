FROM node:latest

RUN mkdir -p /usr/src/app/upload

WORKDIR /usr/src/app

COPY ./server/package.json /usr/src/app/

RUN npm install

COPY ./server/app.js /usr/src/app/
COPY ./server/src /usr/src/app/src


CMD ["node", "app.js"]
