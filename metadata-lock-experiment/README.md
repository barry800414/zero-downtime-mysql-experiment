
# Table Metadata lock experiment
This experiment demonstrates that ALTER TABLE always need exclusive metadata lock, no matter using which algorithm.
If there is long running transaction, ALTER TABLE will be easily blocked.

## Experiment Steps 
1. Download [mysql_random_data_load](https://github.com/Percona-Lab/mysql_random_data_load/releases) according to your os version
2. `mkdir -p ./db; docker-compose up`
3. open new terminal for generating test data: `./mysql_random_data_load -h 127.0.0.1 -P 3306 -u user -p 0000 demo user 1000`
4. open new mysql client (A) by `mysql -h 127.0.0.1 -uroot -p0000 -D demo` and submit transaction request: `START TRANSACTION; DELETE FROM user WHERE 1=1;`
5. open new mysql client (B) for running alter table:
    ```alter table user add email varchar(128) not null default '', algorithm=inplace;```
    You will find that you are blocked, no matter using copy/inplace/instant algorithm
6. open new mysql client (C) for seeing process list: `show processlist;`, you will see `Waiting for table metadata lock`
7. At client A: `rollback;` Then add index operation will be immediately done.
