
HOST=$1
USER=$2
PASSWORD=$3
DATABASE=$4
DURATION=1

while :
do
	mysql -D $DATABASE -h $HOST -u $USER --password=$PASSWORD < transaction_write.sql;
    mysql -D $DATABASE -h $HOST -u $USER --password=$PASSWORD < read.sql;
    mysql -D $DATABASE -h $HOST -u $USER --password=$PASSWORD < transaction_delete.sql;
    sleep $DURATION;
done
