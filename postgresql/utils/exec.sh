#!/bin/bash

# sudo -E docker exec -it postgresql_psql_postgis_db_1 /bin/bash
container=${1:-skynet_db}
sudo -E docker exec -it $container /bin/bash
