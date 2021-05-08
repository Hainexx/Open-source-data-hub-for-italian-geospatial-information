#!/bin/bash

# POSTRGRES DATABASE
psql --username "postgres" --dbname "postgres" <<-EOSQL
CREATE DATABASE skynet OWNER postgres;
EOSQL

echo "Initializing database from scratch"

psql --username postgres --dbname skynet -f db.sql