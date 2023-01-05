
import pymysql.cursors
import random, string

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='0000',
                             database='demo',
                             cursorclass=pymysql.cursors.DictCursor)

if __name__ == '__main__':
    with connection:
        while True:
            username = ''.join([random.choice(string.ascii_letters) for i in range(0, 32)])
            password = ''.join([random.choice(string.ascii_letters) for i in range(0, 64)])

            with connection.cursor() as cursor:            
                # Create a new record
                sql = "INSERT INTO `user` (`username`, `password`) VALUES (%s, %s)"
                try:
                    cursor.execute(sql, (username, password))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()
                except:
                    pass

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `user` WHERE `username`=%s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                print(result)