#!/usr/bin/env bash
airflow db init
airflow users create -r Admin -u admin -e grace.k.susanto@biola.edu -f admin -l user -p admin1234
airflow webserver
airflow scheduler