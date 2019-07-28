#!/usr/bin/env bash

/usr/bin/mysqld_safe &
sleep 3
mysql -u root -pnoflaghere < db.sql
