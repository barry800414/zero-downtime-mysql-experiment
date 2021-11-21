
CHANGE MASTER TO MASTER_HOST='leader.io', MASTER_USER='repl', MASTER_PASSWORD='repl';
start slave;

GRANT ALL ON *.* TO user@'%';