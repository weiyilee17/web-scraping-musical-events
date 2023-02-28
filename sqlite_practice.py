from sqlite3 import connect

# Establish a connection and a cursor
connection = connect('database.db')
cursor = connection.cursor()

# Query all data based on a condition
cursor.execute('SELECT * FROM events WHERE band="Lions"')
lion_rows = cursor.fetchall()
# print(lion_rows)

# Query certain columns based on a condition
cursor.execute('SELECT band, date FROM events WHERE date="2088.10.15"')
band_date_rows = cursor.fetchall()
# print(band_date_rows)

# Insert new rows
new_rows = [
    ('Cats', 'Cat City', '2088.10.17'),
    ('Rats', 'Rat City', '2088.10.17')
]

cursor.executemany('INSERT INTO events VALUES (?, ?, ?)', new_rows)
# Write changes to database
connection.commit()



