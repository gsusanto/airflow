# airflow
Run in a local environment by going into the root directory and execute:
```console
docker-compose up --build
```
After Airflow webserver is running, open Airflow in your local browser and go to:
```
localhost:8080
```
with username: `admin`
and password: `admin1234`  
### Set Airflow Variable
Set Variable for connection to Postgresql database in Airflow by going to Admin > Variable with:  
```
Key: data_dev_connection
Value: "postgresql+psycopg2://airflow:airflow@postgres/airflow"
```
