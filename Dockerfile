FROM node:12

RUN apt-get update && apt-get install -y apt-utils software-properties-common
RUN apt-get update && apt-get install -y libjpeg-dev libtiff5-dev libpng-dev libfreetype6-dev libgif-dev libgtk-3-dev libxml2-dev libpango1.0-dev libcairo2-dev libspiro-dev libuninameslist-dev python3-dev ninja-build cmake build-essential

RUN rm /usr/bin/python
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN mkdir -p /tmp
WORKDIR /tmp
RUN git clone https://github.com/fontforge/fontforge.git
RUN mkdir -p /tmp/fontforge/build
WORKDIR /tmp/fontforge/build
RUN cmake -GNinja --enable-python-scripting --enable-python-extension --enable-pyextension ..
RUN ninja
RUN ninja install

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
