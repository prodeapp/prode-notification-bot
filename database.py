import os

from sqlalchemy import create_engine
from datetime import datetime

# read database connection url from the enivron variable we just set.
DB_URL = os.environ.get('DATABASE_URL')
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DB_USER = os.environ.get('DATABASE_USER')
DB_NAME = os.environ.get('DATABASE_NAME')


def connect():
    uri = os.environ.get('DATABASE_URL').replace('postgres:', 'postgresql:')
    db = create_engine(uri, echo=False)
    return db.connect()


def create_table():
    cmd_create_action_table = """CREATE TABLE IF NOT EXISTS timestamps (
                                last_timestamp bigint NOT NULL
                                )
                            """
    cmd_init_timestamp = ("INSERT INTO timestamps(last_timestamp) VALUES ("
                          f"{int(datetime.timestamp(datetime.now()))})")

    con = connect()
    try:
        con.execute(cmd_create_action_table)
        con.execute(cmd_init_timestamp)

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
        con = connect()

        result = con.execute("SELECT last_timestamp FROM timestamps;")

        # close the communication with the HerokuPostgres
        last_timestamp = result.fetchone()[0]
        con.close()
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
        con = connect()

        con.execute(f"UPDATE timestamps SET last_timestamp={int(timestamp)}")
        con.close()
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
    # from dotenv import load_dotenv
    # load_dotenv()

    # create_table()
    ts = int(datetime.timestamp(datetime.now())) + 10000
    print('writing ts: ', ts)
    write_last_timestamp(ts)
    print(read_last_timestamp())
