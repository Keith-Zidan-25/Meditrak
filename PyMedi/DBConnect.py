import psycopg2

def connect_to_database():
    try:
        db = psycopg2.connect(
            database = '',
            user = 'postgres',
            password = '',
            host = '127.0.0.1',
            port = '5342'
            )
        return db
    except psycopg2.errors as error:
        print(error)
