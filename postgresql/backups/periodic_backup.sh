#!/bin/bash

datenew=$(date +%Y_%m_%d)    
# Get 7 days ago in Alpine is strange
dateold=$(date -d "@$(($(date +%s) - 604800))" +%Y_%m_%d)

echo "Start backup for date ${datenew}" 

# New backup
pg_dumpall > backups/server_${datenew}.sql -U skynet_sa

# Check if exists at least one backup
count=$(ls -1 backups/*.sql | wc -l)
if [ $count != 0 ]; then
    # Delete 7 days old backup
    if [ -e backups/server_${dateold}.sql ]; then
        echo "Remove backup for date %{dateold}" 
        rm backups/server_${dateold}.sql
    fi
fi