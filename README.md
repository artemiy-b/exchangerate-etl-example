# exchangerate-etl-example

```bash
docker-compose up airflow-init

docker-compose up -d

docker-compose run airflow-cli airflow variables set pg_ip $(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aqf "name=exchangerate-etl-example_db_1"))

docker-compose run airflow-cli airflow dags unpause best_dag_ever
```


удалить все

docker-compose down --volumes --rmi all

