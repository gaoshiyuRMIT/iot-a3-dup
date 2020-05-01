#! /bin/bash

# prerequisite: 
# if venv is not set up, you need to set $python -- which python to use

for conf_file in admin-app/.flaskenv admin-app/config.py cloud-db-api/config.py
do
    if [ ! -f $conf_file ]
    then
        echo "config file $conf_file is required"
        exit 1
    fi
done

if ( [ ! -d cloud-db-api/venv ] || [ ! -d admin-app/venv ] ) && [ -z $python ]
then
    echo "pls set environment viable $python. e.g. export python=python3.7"
    exit 1
fi

cd cloud-db-api
if [ ! -d venv ]; then
    $python -m venv venv
    . venv/bin/activate
    pip install --upgrade pip > pip.log 2>&1
    pip install --upgrade -r requirements.txt > pip.log 2>&1
else
    . venv/bin/activate
fi
flask run > flask.log 2>&1 & 
api_pid=$! 
deactivate
echo "* cloud-db-api successfully started"

cd ../admin-app
if [ ! -d venv ]; then
    $python -m venv venv
    . venv/bin/activate
    pip install --upgrade pip > pip.log 2>&1
    pip install --upgrade -r requirements.txt > pip.log 2>&1
else
    . venv/bin/activate
fi
flask run --host=0.0.0.0 > flask.log 2>&1 &
website_pid=$!
echo "* admin-app successfully started"

# echo "API PID: $api_pid, website PID: $website_pid"
# echo "to stop both background processes: kill $api_pid $website_pid"

trap "kill $api_pid $website_pid" SIGINT

wait $api_pid
wait $website_pid
