#!/bin/bash

sudo apt install python3-pip

pip install -r scripts/requirements.txt

python scripts/downloader.py --region lombardia

cp -r scripts/raw_data postgresql/files/

sudo -E docker exec -it skynet_db sh /files/load_raw_data.sh