#!/bin/bash
# Author: Alex Gomes
# Description: The purpose is to stop the entire process.

CELERY_PS="celery -A modules.apis.v1.db_controller.worker worker --loglevel=info"
API_PS="python3 api.py"
FE_PS="ng serve"

cd back-end
echo "Stopping the API..."
pkill -f "$API_PS"
echo "Stopping the Celery..."
pkill -f "$CELERY_PS"
echo "Stopping Redis..."
sudo service redis-server stop
echo "Stopping Angular..."
pkill -f "$FE_PS"
cd  ..