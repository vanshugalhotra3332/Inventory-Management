import mysql.connector as mysql
from variables import password, database, user, host
from initialize import init_db, init_tables


try:
    connection = mysql.connect(
        user=user,
        host=host,
        password=password,
        database=database
    )
    cursor = connection.cursor()
    
except mysql.errors.ProgrammingError:
    print(f"Creating Database.......{database}")
    init_db(database=database)
    
    connection = mysql.connect(
        user=user,
        host=host,
        password=password,
        database=database
    )
    
    cursor = connection.cursor()
    init_tables()
    




