#!/bin/bash

pip install -r scripts/requirements.txt

python scripts/downloader.py --region lombardia

cp -r scripts/raw_data postgresql/files/

sh postgresql/utils/load_raw_data.sh