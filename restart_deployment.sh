#!/bin/bash

## Use cache:
ssh ids3 'cd /data/deploy-ids-tests/RD-FAIRmetric-F4 ; git pull ; docker-compose -f docker-compose.prod.yml up --force-recreate --build -d'

## Without cache:
# ssh ids3 'cd /data/deploy-ids-tests/RD-FAIRmetric-F4 ; git pull ; docker-compose -f docker-compose.prod.yml build ; docker-compose down ; docker-compose -f docker-compose.prod.yml up --force-recreate -d'