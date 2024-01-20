#!/bin/bash
# init-db.sh: Script to initialize PostgreSQL database if it doesn't exist

set -e

# Function to check if the database exists
database_exists() {
  psql -lqt | cut -d \| -f 1 | grep -qw "$POSTGRES_DB"
}

# Wait for PostgreSQL to start
until pg_isready -h "$POSTGRES_DB" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Check if the database exists, and create it if it doesn't
if ! database_exists; then
  echo "Database $POSTGRES_DB does not exist. Creating..."
  createdb -U "$POSTGRES_USER" -O "$POSTGRES_USER" "$POSTGRES_DB"
  echo "Database $POSTGRES_DB created."
fi
