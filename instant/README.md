

1. `docker-compose up`
2. open new terminal for generating test data: `./mysql_random_data_load -h 127.0.0.1 -P 3306 -u user -p 0000 demo user 1000`
3. open new mysql client (A) for generating transaction: `START TRANSACTION; DELETE FROM user WHERE 1=1;`
4. open new mysql client (B) for running alter table who supports instant algorithm:
    ```alter table user add email varchar(128) not null default '', algorithm=instant;```
