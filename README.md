# sqLite-Lec5-Jan-05-25
python connect to SQLite
* added cursor.executemany with 1 query with a list of values
  ```
  data = [
    ('Avokado', 5),
    ('Milk', 2),
    ('Bread', 3),
    ('Chocolate', 8),
    ('Bamba', 5),
    ('Orange', 10)
]
cursor.executemany('''
    INSERT INTO shopping (name, amount)
    VALUES (?, ?)
''', data)
print('Data inserted')
  ```
