# exchangerate-etl-example

Для запуска выполнить следующие команды
```bash
docker-compose up airflow-init

docker-compose up -d

docker-compose run airflow-cli airflow variables set pg_ip $(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aqf "name=exchangerate-etl-example_db_1"))

docker-compose run airflow-cli airflow dags unpause exchange_rate
```

Для остановки и удаления образов

```bash
docker-compose down --volumes --rmi all
```
