import psycopg2
conn = psycopg2.connect(
    database="items", user="postgres", password="1234", host="127.0.0.1", port="5432"
)

cursor = conn.cursor()

cursor.execute("select * from items")

cursor.execute("insert into items values(%s, %s, %s, %s, %s)", (1, "apple", "hi", "hello", "beans"))

cursor.execute("select * from items")

print(cursor.fetchall())
conn.close()