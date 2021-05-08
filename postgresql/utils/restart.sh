#!/bin/bash

sudo docker-compose down $@
sleep 3
sudo docker-compose build $@
sleep 3
sudo docker-compose up -d $@