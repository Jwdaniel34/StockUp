#!/bin/sh

/usr/local/bin/gunicorn stockup_project.wsgi:application -w 2 -b :8000

if [ "$NAMEDB_POST" = "$NAMEDB_POST" ]
then 
    echo "Waiting for postgress...."

    while ! nc -z $HOST_POST $PORT_POST; do
        sleep 0.1
    done 

    echo "PostgresSQL started"

fi 

if [ "$NAMEDB_MYSQL" = "$NAMEDB_MYSQL" ]
then 
    echo "Waiting for mysql...."

    while ! nc -z $HOST_MYSQL $PORT_MYSQL; do
        sleep 0.1
    done 

    echo "MySQL started"

fi 



exec "$@"