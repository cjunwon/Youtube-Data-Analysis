import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

def get_db_info():

    """
    Extracts database information from .env file

    Params:
    --------

    Return:
    --------
    All components of MySQL database required to initiate connection to the database as string objects
    """

    load_dotenv()

    host_name = os.getenv('host_name')
    dbname = os.getenv('dbname')
    schema_name = os.getenv('schema_name')
    port = os.getenv('port')
    username = os.getenv('username')
    password = os.getenv('password')

    return host_name, dbname, schema_name, port, username, password



def connect_to_db(username, password, host_name, schema_name, port):

    """
    Connects to database

    Params:
    --------
    username: database username
    password: database password
    host_name: database host name/address
    schema_name: name of MySQL schema
    port: port number of database

    Return:
    --------
    MySQLConnection constructor from database information provided as paramaters

    """

    try:
        cnx = mysql.connector.connect(user=username,
                                    password=password,
                                    host=host_name,
                                    database=schema_name,
                                    port=port)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print('Connected to Database')
        return cnx