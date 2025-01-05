import sqlite3


def connect_to_db() -> sqlite3.Connection:
    """

    :rtype: sqlite3.Connection
    """
    try:
        db_name: str = "C:/Users/Shani/OneDrive/Documents/school/Ecom/SQL/sqLite-Lec4-Dec-22-24/dec-22-2024.db"
        connector = sqlite3.connect(db_name)
        connector.row_factory = sqlite3.Row  # allow to address the values by column name
        return connector
    except sqlite3.Error as e:
        print(e)
        raise "failed connection to db with error" + (' '.join(e.args))


def execute_query_fetch_all(connector, query):
    try:
        cursor = connector.cursor()  # pointer where you are now,to read and write

        cursor.execute(query)
        rows = cursor.fetchall()  # after the result, the cursor "moves" to the end of the table
        cursor.execute(query)  # so need to execute again to do fetchone again
        row = cursor.fetchone()
        print(tuple(row))
        return rows
    except sqlite3.OperationalError as e:
        raise e


def execute_query_create(connector, query):
    try:
        cursor = connector.cursor()  # pointer where you are now,to read and write
        query = '''CREATE TABLE Departments (
                    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    building TEXT NOT NULL,
                    budget INTEGER DEFAULT 100000
                    );
                '''
        cursor.execute(query)
        connector.commit()  ## this will write the changes to the DB
    except sqlite3.OperationalError as e:
        raise e
    finally:
        connector.close()


def execute_query_delete_update_insert_create(connector, query):
    try:
        cursor = connector.cursor()  # pointer where you are now,to read and write
        query = "delete from Employees where id=?"  # the ? will be replaced by the given parameters below
        parameter = 1
        cursor.execute(query, parameter)
        connector.commit()  ## this will write the changes to the DB
    except sqlite3.OperationalError as e:

        raise e


def run_first_query():
    my_connector = None
    try:

        my_connector = connect_to_db()
        query: str = '''select * 
                        from Employees'''
        result = execute_query_fetch_all(my_connector, query)
        for row in result:
            print("as dict:", dict(row))
            print("as tuple:", tuple(row))
            print("as set:", set(row))
            print("as list:", list(row))
            print(f"name:{row['name']}")
        result_list = [tuple(row) for row in result]
        # connector = connect_to_db()#need to open the connector again
        execute_query_create(my_connector, query)
    except Exception as e:
        print(e)
        return
    finally:
        if my_connector is not None:
            my_connector.close()


if __name__ == "__main__":
    run_first_query()
