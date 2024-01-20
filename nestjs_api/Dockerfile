# Set specific Versions for Node and pnpm
ARG NODE_VERSION=20.9.0-alpine3.18
ARG PNPM_VERSION=8.10.5

# Base stage with Node.js
################################################################################
FROM node:${NODE_VERSION} as base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
# Set working directory for all build stages.
WORKDIR /usr/src/app

ENV DOCKERIZE_VERSION v0.7.0

# Install dockerize
ENV DOCKERIZE_VERSION v0.7.0

RUN apk update --no-cache && apk add --no-cache wget openssl
RUN wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin
RUN apk del wget
# Install dependencies
FROM base as deps

COPY --chown=node:node nest-cli.json ./
COPY --chown=node:node tsconfig.json ./
COPY --chown=node:node package*.json pnpm-lock.yaml ./
COPY --chown=node:node ./prisma ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --no-frozen-lockfile

################################################################################
# Create a stage for building the application.
FROM deps as build
COPY --chown=node:node . .
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile
RUN npx prisma generate
RUN pnpm run build

################################################################################
# Create a new stage to run the application with minimal runtime dependencies
FROM base as final
RUN apk add --update dumb-init postgresql-client
ENV NODE_ENV production

USER node

COPY --chown=node:node --from=build /usr/src/app/package*.json /usr/src/app/pnpm-lock.yaml ./

COPY --chown=node:node --from=build /usr/src/app/node_modules/ ./node_modules
COPY --chown=node:node --from=build /usr/src/app/dist ./dist

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD [ "node", "healthceck.js" ]

# Run the application.
CMD ["dumb-init", "node", "dist/main"]
