#!/bin/bash

# TODO implement multiple loading for different regions
psql --username "postgres" --dbname "skynet" <<-EOSQL
COPY stg_buildings_footprints FROM '/files/raw_data/geoportale_lombardia/complete_dataset.csv' WITH (FORMAT csv);
EOSQL