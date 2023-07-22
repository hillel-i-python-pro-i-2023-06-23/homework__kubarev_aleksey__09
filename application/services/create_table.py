from application.services.db_connection import DBConnection


def create_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                phone_id INTEGER NOT NULL PRIMARY KEY ,
                contact_name VARCHAR NOT NULL,
                phone_value VARCHAR NOT NULL
                )
            """
            )
