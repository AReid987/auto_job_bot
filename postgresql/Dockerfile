FROM postgres:latest

COPY ./init-db.sh /docker-entrypoint-initdb.d/init.sql
EXPOSE 5432
