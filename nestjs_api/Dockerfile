# SET Versions for Node and pnpm
ARG NODE_VERSION=20.9.0
ARG PNPM_VERSION=8.10.5

################################################################################
# Use node image for base image for all stages.
FROM node:${NODE_VERSION}-alpine as base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
# Set working directory for all build stages.
WORKDIR /usr/src/app

# Install pnpm
# RUN --mount=type=cache,target=/root/.npm \
#     npm install -g pnpm@${PNPM_VERSION}
################################################################################
# Create a stage for installing production dependecies.
FROM base as deps

# Copy nest-cli.json
COPY --chown=node:node nest-cli.json ./

# Copy tsconfig
COPY --chown=node:node tsconfig.json ./

# Copy package.json and pnpm-lock.yaml
COPY --chown=node:node package.json ./
COPY --chown=node:node pnpm-lock.yaml ./

COPY --chown=node:node ./prisma ./

RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --no-frozen-lockfile

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.local/share/pnpm/store to speed up subsequent builds.
# Leverage bind mounts to package.json and pnpm-lock.yaml to avoid having to copy them
# into this layer.
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=pnpm-lock.yaml,target=pnpm-lock.yaml \
    --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --prod --frozen-lockfile

################################################################################
# Create a stage for building the application.
FROM deps as build

# # Copy the rest of the source files into the image.
COPY --chown=node:node . .

# Download additional development dependencies before building, as some projects require
# "devDependencies" to be installed to build. If you don't need this, remove this step.
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=pnpm-lock.yaml,target=pnpm-lock.yaml \
    --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile

# Generate Prisma Client
RUN npx prisma generate

RUN pnpm run prismaDev
# Run the build script.
RUN pnpm run build

################################################################################
# Create a new stage to run the application with minimal runtime dependencies
# where the necessary files are copied from the build stage.
FROM base as final

RUN apk add --update dumb-init
RUN apk add --no-cache postgresql-client

# Use production node environment by default.
ENV NODE_ENV production

# Run the application as a non-root user.
USER node


# Copy the production dependencies from the deps stage
COPY --chown=node:node --from=deps /usr/src/app/node_modules ./node_modules
# Copy package.json so that package manager commands can be used.

COPY --chown=node:node --from=build /usr/src/app/package.json ./
COPY --chown=node:node --from=build /usr/src/app/pnpm-lock.yaml ./
# Copy the built application from the build stage into the image.
COPY --chown=node:node --from=build /usr/src/app/dist ./dist

# Copy Prisma
COPY --chown=node:node --from=build /usr/src/app/node_modules/@prisma/client ./node_modules/@prisma/client

COPY --chown=node:node --from=build /usr/src/app/node_modules/.pnpm/@prisma+client@5.8.0_prisma@5.8.0/node_modules ./node_modules/.pnpm/@prisma+client@5.8.0_prisma@5.8.0/node_modules

# Wait for the PostgreSQL db to be ready before starting server
COPY --chown=node:node wait-for-postgres.sh /usr/src/app/wait-for-postgres.sh

RUN chmod +x /usr/src/app/wait-for-postgres.sh
# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD ["dumb-init", "node", "dist/main"]