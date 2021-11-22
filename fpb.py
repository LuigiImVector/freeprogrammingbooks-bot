import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor=conn.cursor()

#cursor.execute('INSERT INTO fpb(id) VALUES (7437246);')
#cursor.execute('DELETE FROM fpb;')

username = "LuigiImVector"

categoryName = cursor.execute('SELECT choice FROM fpb WHERE username=%s', (username,))
categoryName = categoryName.fetchall()
categoryName = ''.join(categoryName[0])
category = "https://raw.githubusercontent.com/EbookFoundation/free-programming-books/main/" + categoryName

print(category)

#conn.commit()
