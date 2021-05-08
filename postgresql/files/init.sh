#!/bin/bash

######################################################################
## NEW DATABASE
# psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
# EOSQL

######################################################################
# POSTRGRES DATABASE
psql --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
CREATE DATABASE skynet OWNER postgres;
EOSQL