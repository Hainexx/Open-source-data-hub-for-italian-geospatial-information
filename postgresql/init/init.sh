#!/bin/bash

echo "Initializing database from scratch"

psql --username postgres --dbname skynet -f db.sql