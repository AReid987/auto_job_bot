#!/bin/bash

# shellcheck disable=SC1091

# Function to check if script is run with superuser privileges
check_superuser() {
  if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root or with sudo privileges."
    exit 1
  fi
}

# Function to check if PostgreSQL is installed
check_postgres_installed() {
  if command -v psql >/dev/null 2>&1; then
    echo "PostgreSQL is already installed."
    return 0
  else
    return 1
  fi
}

# Function to find PostgreSQL data directory
find_pg_data_directory() {
  # Attempt to use pg_config to find the data directory
  local pg_data_dir
  if command -v pg_config >/dev/null 2>&1; then
    pg_data_dir=$(pg_config --sharedir)
    if [ -n "$pg_data_dir" ]; then
      echo "$pg_data_dir"
      return
    fi
  fi

  # Fallback to common directory paths
  for dir in /var/lib/postgresql/*/main /usr/local/var/postgres; do
    if [ -d "$dir" ]; then
      echo "PostgreSQL data directory found at $dir"
      return
    fi
  done

  echo "Failed to locate PostgreSQL data directory."
  exit 1
}
# Function to load .env file from parent directory
load_env() {
  if [ -f "../.env" ]; then
    export "$(grep -v '^#' ../.env | xargs)"
  else
    echo "No .env file found in the parent directory."
    exit 1
  fi
}

# Function to start PostgreSQL service
start_postgres_service() {
  local pg_data_dir
  pg_data_dir=$(find_pg_data_directory)
  echo "Starting PostgreSQL service using data directory $pg_data_dir..."
  pg_ctl -D "$pg_data_dir" start || {
    echo "Failed to start PostgreSQL service."
    exit 1
  }
}

# Function to check if the database exists
does_db_exist() {
  if psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    return 0
  else
    return 1
  fi
}

# Function to create the database
create_db() {
  echo "Creating database '$DB_NAME'..."
  psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" || {
    echo "Failed to create database. Ensure '$DB_USER' has necessary permissions."
    exit 1
  }
}

# Function to grant necessary permissions to PostgreSQL user
grant_permissions() {
  echo "Granting necessary permissions to user '$DB_USER'..."
  psql -c "ALTER USER $DB_USER CREATEDB;" || {
    echo "Failed to grant necessary permissions to user '$DB_USER'."
    exit 1
  }
}

# Function to install PostgreSQL on Debian-based systems
install_postgres_debian() {
  echo "Updating package lists..."
  sudo apt-get update
  echo "Installing PostgreSQL..."
  sudo apt-get install postgresql postgresql-contrib || {
    echo "Failed to install PostgreSQL."
    exit 1
  }
}

# Function to install PostgreSQL on RedHat-based systems
install_postgres_redhat() {
  echo "Updating package lists..."
  sudo yum update
  echo "Installing PostgreSQL..."
  sudo yum install postgresql-server postgresql-contrib || {
    echo "Failed to install PostgreSQL."
    exit 1
  }
}

# Detecting OS type
OS_TYPE=$(uname -s)

# check_superuser

case "$OS_TYPE" in
Linux*)
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    case "$ID" in
    ubuntu | debian | linuxmint)
      if ! check_postgres_installed; then
        install_postgres_debian
      fi
      ;;
    fedora | centos | rhel)
      if ! check_postgres_installed; then
        install_postgres_redhat
      fi
      ;;
    *)
      echo "Unsupported Linux distribution for automated PostgreSQL installation."
      ;;
    esac
  else
    echo "Unable to detect Linux distribution."
  fi
  ;;
Darwin*)
  echo "Checking for PostgreSQL on MacOS..."
  if ! check_postgres_installed; then
    if command -v brew >/dev/null 2>&1; then
      brew update
      brew install postgresql || {
        echo "Failed to install PostgreSQL."
        exit 1
      }
    else
      echo "Homebrew not found. Please install Homebrew first."
    fi
  fi
  start_postgres_service

  ;;
*)
  echo "Unsupported Operating System. Please download and install PostgreSQL manually."
  ;;
esac

load_env

# Grant necessary permissions to user
grant_permissions

if ! does_db_exist; then
  create_db
else
  echo "Database '$DB_NAME' already exists."
fi
