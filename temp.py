import sqlite3

conn = sqlite3.connect("Users.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE Users
                  (id INT PRIMARY KEY,
                   location int)
               """)
conn.commit()