
## Preparation
0. Download mysql_random_data_load from https://github.com/Percona-Lab/mysql_random_data_load
1. Run mysql 8.0 locally by `mkdir -p ./db; docker-compose up`
2. Generate 1 million test data: `./mysql_random_data_load -h 127.0.0.1 -P 3306 -u user -p 0000 demo user 1000000`
3. Connect mysql: `mysql -h 127.0.0.1 -uroot -p0000 -D demo`

## Compare performance of each algorithm
```
alter table user add email varchar(128) not null default '', algorithm=copy;
alter table user drop email;
alter table user add email varchar(128) not null default '', algorithm=inplace;
alter table user drop email;
alter table user add email varchar(128) not null default '', algorithm=instant;
alter table user drop email;
```
