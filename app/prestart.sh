#!/usr/bin/env bash

redis-server &
celery -A app.celery worker &
/usr/bin/mysqld_safe &
sleep 5
mysql -u root -ppassword < db.sql
