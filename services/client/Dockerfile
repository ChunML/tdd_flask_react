FROM node:12.10.0-alpine

WORKDIR /usr/src

ENV path /usr/src/node_modules/.bin:$PATH

COPY package.json .
COPY yarn.lock .
RUN yarn
RUN yarn global add react-scripts@2.1.8 --silent

COPY . .

CMD ["yarn", "start"]