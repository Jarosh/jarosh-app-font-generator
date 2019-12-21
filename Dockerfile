FROM node:12-alpine

RUN npm install -g pm2

RUN mkdir -p /home/node/app
RUN mkdir /home/node/app/tmp
RUN chown -R node:node /home/node/app

WORKDIR /home/node/app

USER node
COPY . .

RUN npm install

EXPOSE 8080

CMD [ "pm2-runtime", "pm2.config.js" ]
