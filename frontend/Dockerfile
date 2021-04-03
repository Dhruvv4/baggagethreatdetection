FROM node:14-alpine AS base
RUN apk add --no-cache git

WORKDIR /frontend

COPY package.json /frontend

RUN npm install

COPY . /frontend

RUN npm run build