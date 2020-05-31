#! /bin/bash

# prerequisite: 
# if venv is not set up, you need to set $python -- which python to use

for conf_file in customer-app/.flaskenv customer-app/config.py cloud-db-api/config.py customer-app/credentials.json
do
    if [ ! -f $conf_file ]
    then
        echo "config file $conf_file is required"
        exit 1
    fi
done

if ( [ ! -d cloud-db-api/venv ] || [ ! -d customer-app/venv ] ) && [ -z $python ]
then
    echo "pls set environment variable $python. e.g. export python=python3.7"
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
FLASK_DEBUG=0 python -m flask run > flask.log 2>&1 & 
api_pid=$! 
deactivate
echo "* cloud-db-api successfully started"

cd .. customer-app
if [ ! -d venv ]; then
    $python -m venv venv
    . venv/bin/activate
    pip install --upgrade pip > pip.log 2>&1
    pip install --upgrade -r requirements.txt > pip.log 2>&1
else
    . venv/bin/activate
fi
FLASK_DEBUG=0 python -m flask run --host=0.0.0.0 > flask.log 2>&1 &
website_pid=$!
deactivate
echo "* customer-app successfully started"

# echo "API PID: $api_pid, website PID: $website_pid"
# echo "to stop both background processes: kill $api_pid $website_pid"

trap "kill $api_pid $website_pid" SIGINT

api_exited=0
website_exited=0
while [ $api_exited -ne 1 ] || [ $website_exited -ne 1 ]
do
    if [ $api_exited -ne 1 ] && ! ps | grep "^$api_pid" > /dev/null
    then
        api_exited=1
        if ! wait $api_pid
        then
            echo "* cloud-db-api exited with an error"
        fi
    fi
    if [ $website_exited -ne 1 ] && ! ps | grep "^$website_pid" > /dev/null
    then
        website_exited=1
        if ! wait $website_pid
        then
            echo "* customer-app exited with an error"
        fi
    fi
    sleep 1
done

