import mysql.connector as mysql
from variables import password, database, user, host


connection = mysql.connect(
    user=user,
    host=host,
    password=password,
    database=database
)
cursor = connection.cursor()



