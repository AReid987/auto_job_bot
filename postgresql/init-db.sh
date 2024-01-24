#!/bin/bash
# init-db.sh: Script to initialize PostgreSQL database if it doesn't exist

set -e

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Function to print green
echo_green() {
  echo -e "${GREEN}$1${NC}"
}

# Function to print red
echo_red() {
  echo -e "${RED}$1${NC}"
}
# Function to check if the database exists
database_exists() {
  psql -lqt | cut -d \| -f 1 | grep -qw "$POSTGRES_DB"
}

# Wait for PostgreSQL to start
until pg_isready -h "$POSTGRES_DB" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo_red "Waiting for PostgreSQL to start..."
  sleep 2
done

# Check if the database exists, and create it if it doesn't
if ! database_exists; then
  echo_red "Database $POSTGRES_DB does not exist. Creating..."
  createdb -U "$POSTGRES_USER" -O "$POSTGRES_USER" "$POSTGRES_DB"
  echo_green "Database $POSTGRES_DB created."
fi
