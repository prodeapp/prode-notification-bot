import os

import psycopg2
from datetime import datetime

# read database connection url from the enivron variable we just set.
DATABASE_URL = os.environ.get('DATABASE_URL')


def create_table():
    cmd_create_action_table = """CREATE TABLE timestamps (
                                last_timestamp bigint NOT NULL
                                )
                            """
    cmd_init_timestamp = ("INSERT INTO timestamps(last_timestamp) VALUES ("
                          f"{int(datetime.timestamp(datetime.now()))})")

    con = None
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()
        cur.execute(cmd_create_action_table)
        cur.execute(cmd_init_timestamp)
        # close the communication with the HerokuPostgres
        cur.close()
    except Exception as error:
        print('Could not connect to the Database.')
        print('Cause: {}'.format(error))

    finally:
        # close the communication with the database server by calling the close()
        if con is not None:
            con.close()
            print('Database connection closed.')


def read_last_timestamp():
    con = None
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()
        cur.execute("SELECT last_timestamps FROM timestamps")

        # close the communication with the HerokuPostgres
        last_timestamp = cur.fetchone()
        cur.close()
    except Exception as error:
        print('Could not connect to the Database.')
        print('Cause: {}'.format(error))
        last_timestamp = None
    finally:
        # close the communication with the database server by calling the
        # close()
        if con is not None:
            con.close()
            print('Database connection closed.')
    return last_timestamp


def write_last_timestamp(timestamp):
    con = None
    try:
        # create a new database connection by calling the connect() function
        con = psycopg2.connect(DATABASE_URL)

        #  create a new cursor
        cur = con.cursor()
        cur.execute(f"UPDATE timestamps SET last_timestamp={int(timestamp)}")

        cur.close()
    except Exception as error:
        print('Could not connect to the Database.')
        print('Cause: {}'.format(error))
    finally:
        # close the communication with the database server by calling the
        # close()
        if con is not None:
            con.close()
            print('Database connection closed.')


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    create_table()
    read_last_timestamp()
