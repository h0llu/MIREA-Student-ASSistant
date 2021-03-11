import sqlite3

def create(user_id):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE Users
                  (id INT PRIMARY KEY,
                   location int)с
                   """)

def check(user_id):
