#!/usr/bin/env bash

celery -A app.celery worker &
redis-server &
/usr/bin/mysqld_safe &
sleep 5
mysql -u root -ppassword < db.sql
