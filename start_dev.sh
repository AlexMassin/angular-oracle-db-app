#!/bin/bash
# Author: Alex Gomes
# Description: The purpose is to start the entire process.

START_CELERY="celery -A modules.apis.v1.db_controller.worker worker --loglevel=info"
START_API="python3 api.py"
START_FE="npm start"

function run_detached() {
    eval cmd="$1"
    echo "Running: ${cmd}"
    nohup ${cmd} &>/dev/null &
}

cd back-end
sudo service redis-server start
run_detached "\${START_API}"
run_detached "\${START_CELERY}"
cd  ..
cd front-end
run_detached "\${START_FE}"
cd ..
echo "Front End: localhost:4200"
echo "Back End: localhost:5000"
echo "Note: Angular can take around a minute to fully start up depending on your machine."