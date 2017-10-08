FROM node:boron-alpine
MAINTAINER PeRDy (http://www.perdy.top)

ENV APP=barrenero-miner-storj

RUN apk add --no-cache bash g++ git make openssl-dev python vim && \
node --version && \
npm --version && \
python --version && \
npm install --global storjshare-daemon && \
npm cache clean && \
apk del git openssl-dev python vim && \
rm -rf /var/cache/apk/* && \
rm -rf /tmp/npm* && \
storjshare --version

# Create project dirs
RUN mkdir -p /srv/apps/$APP/logs
RUN mkdir -p /srv/apps/$APP/storage
WORKDIR /srv/apps/$APP

# Copy application
COPY . /srv/apps/$APP/

ENTRYPOINT ["storjshare"]