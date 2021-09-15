#!/bin/sh

if [ "$NAMEDB_POST" = "sparrowsuserdb" ]
then 
    echo "Waiting for postgress...."

    while ! nc -z $HOST_POST $PORT_POST; do
        sleep 0.1
    done 

    echo "PostgresSQL started"

fi 

if [ "$NAMEDB_MYSQL" = "dividends" ]
then 
    echo "Waiting for mysql...."

    while ! nc -z $HOST_MYSQL $PORT_MYSQL; do
        sleep 0.1
    done 

    echo "MySQL started"

fi 



exec "$@"