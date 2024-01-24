#!/bin/bash
# create-db.sh: Ensure PostgreSQL database exists

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

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_DB" -U "$POSTGRES_USER" -c '\q'; do
  echo_red "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo_green "PostgreSQL is up - checking if database exists"

# Create the database if it doesn't exit
PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "$POSTGRES_USER" <<-EOSQL
  SELECT 'CREATE DATABASE $POSTGRES_DB'
  WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRES_DB')\gexec
EOSQL

if ! mycmd; then
  echo_green "Database $POSTGRES_DB created or already exists"
else
  echo_red "Failed to create database $POSTGRES_DB"
fi
