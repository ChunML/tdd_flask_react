FROM node:12.10.0-alpine

WORKDIR /usr/src/app

ENV path /usr/src/app/node_modules/.bin:$PATH

COPY package.json .
COPY package-lock.json .
RUN npm ci
RUN npm install react-scripts@2.1.8 -g --silent

CMD ["npm", "start"]