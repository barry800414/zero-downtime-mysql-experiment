

# Concurrent DML experiment
This experiment demonstrates that ALTER TABLE always need exclusive metadata lock, no matter using which algorithm.
If there is long running transaction, ALTER TABLE will be easily blocked.

## Experiment Steps 
1. Download [mysql_random_data_load](https://github.com/Percona-Lab/mysql_random_data_load/releases) according to your os version
2. `mkdir -p ./db; docker-compose up`
3. open new terminal for generating test data: `./mysql_random_data_load -h 127.0.0.1 -P 3306 -u user -p 0000 demo user 1000000`
4. Run `python dml.py` to continuously inserting new records
5. Open new mysql client by `mysql -h 127.0.0.1 -uroot -p0000 -D demo` for running alter table:
    ```alter table user add email varchar(128) not null default '', algorithm=copy;```
