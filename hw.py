import os
import sqlite3

def connect_to_db():
    try:
        db_name: str = "solution_hw.db"
        if os.path.exists(db_name):
            os.remove(db_name)
        connector = sqlite3.connect(db_name)
        connector.row_factory = sqlite3.Row  # allow to address the values by column name
        return connector
    except sqlite3.Error as e:
        print(e)
        raise "failed connection to db with error" + (' '.join(e.args))

def execute_query(connector, query, parameters=None):
    try:
        cursor = connector.cursor()  # pointer where you are now,to read and write
        print("execute query:", query)
        if parameters is not None:
            return cursor.execute(query, parameters)
        return cursor.execute(query)
    except sqlite3.OperationalError as e:
        raise e

def execute_change_query(connector, query, parameters=None):
    try:
        cursor = connector.cursor()  # pointer where you are now,to read and write
        if parameters is not None:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        connector.commit()  ## this will write the changes to the DB
    except sqlite3.OperationalError as e:
        raise e

def print_results(rows):
    rows_list = [tuple(row) for row in rows]
    for row in rows_list:
        print(row)

def run_homework():
    my_connector = None
    try:
        my_connector = connect_to_db()
        create_query = 'CREATE TABLE shopping(id INTEGER PRIMARY KEY,  name TEXT,amount INTEGER);'
        execute_change_query(my_connector, create_query);
        insert_parameters_list = [(1, 'Avokado', 5), (2, 'Milk', 2),
                                  (3, 'Bread', 3), (4, 'Chocolate', 8),
                                  (5, 'Bamba', 5), (6, 'Orange', 10)];
        for parameters in insert_parameters_list:
            print("will insert the item:", parameters)
            execute_change_query(my_connector, 'INSERT INTO shopping VALUES (?, ?, ?)', parameters)
        rows = execute_query(my_connector, 'SELECT * FROM shopping')
        print_results(rows)
        rows = execute_query(my_connector, 'SELECT * FROM shopping WHERE amount > ?', (5,))
        print_results(rows)
        execute_change_query(my_connector, "DELETE from shopping WHERE name like ?", ('Orange',));
        execute_change_query(my_connector, "UPDATE shopping SET name = ? WHERE name LIKE ?",
                             ('Bisli', 'Bamba'));
        execute_change_query(my_connector, "UPDATE shopping SET amount=? WHERE name LIKE ?",
                             (1, 'Milk',));
        rows = execute_query(my_connector, 'SELECT COUNT(*)from shopping')
        print_results(rows)
        rows = execute_query(my_connector, 'SELECT * FROM shopping WHERE id > ?', (0,))
        print_results(rows)
    except Exception as e:
        print(e)
    finally:
        if my_connector is not None:
            my_connector.close()


if __name__ == "__main__":
    run_homework()
