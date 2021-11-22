import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor=conn.cursor()

#cursor.execute('INSERT INTO fpb(id) VALUES (7437246);')
#cursor.execute('DELETE FROM fpb;')

#conn.commit()

id = 659

username = "LuiginoPaneEVino"

defaultCategory = "books/free-programming-books-langs.md"

cursor.execute('SELECT * FROM fpb WHERE id=%s;', (id,))
   
if cursor.fetchone() is not None:
    print("Username already saved")
else:
    cursor.execute('INSERT INTO fpb(id, username, choice) VALUES (%s, %s, %s);', (id, username, defaultCategory,))
    conn.commit()
    print("Username saved")