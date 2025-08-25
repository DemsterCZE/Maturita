import mysql.connector
import dotenv
import os

dotenv.load_dotenv()


def get_connection():
    return connection_pool.get_connection()

def check_for_table_presence() -> None:
    database = get_connection()
    cursor = database.cursor()
    cursor.execute("SHOW TABLES LIKE 'roles'")
    result2 = cursor.fetchone()
    if result2:
        print("Tabulka roles existuje")
    else:
        cursor.execute('''CREATE TABLE roles(
                       RoleID INT AUTO_INCREMENT PRIMARY KEY,
                       RoleName VARCHAR(20)
                       )
                        ''')
        cursor.execute( '''
                       INSERT INTO roles (RoleName)
                       VALUES ('Admin'),('Player')
                       ''')
        database.commit()


    cursor.execute("SHOW TABLES LIKE 'users'")
    result = cursor.fetchone()
    if result:
        print("tabulka users existuje")
    else:
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(32) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password_hash VARCHAR(128),
                highest_score INT DEFAULT 0,
                RoleID int,
                FOREIGN KEY (RoleID) REFERENCES roles(RoleID)
            )
        """)
        print("Tabulka users vytvořena")

        
        print("Tabulka roles vytvořena")
     
    return


try: 

    db = {
        "host"  : os.getenv("HOST"),
        "user" : os.getenv("USER"),
        "password" : os.getenv("PASSWORD"),
        "database": os.getenv("DATABASE")
    }
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **db)
    check_for_table_presence()
    print("Připojení do databáze bylo úspěšné")
except mysql.connector.Error as E:
    print(E)



