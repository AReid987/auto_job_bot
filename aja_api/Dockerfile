# Description: Dockerfile for the aja_api

# Set specific version of Node and pnpm
ARG NODE_VERSION=20.9.0-alpine3.18
ARG PNPM_VERSION=8.14.2

# BUILD FOR LOCAL DEVELOPMENT

FROM node:${NODE_VERSION} as development

# Set the working directory
WORKDIR /usr/src/app
