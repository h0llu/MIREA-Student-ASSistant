import sqlite3

def create(user_id):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE id = "+str(user_id))
    
    if len(cursor.fetchall())==0:
        cursor.execute('INSERT INTO Users VALUES('+str(user_id)+',0)')
    conn.commit()
    conn.close()

def check(user_id):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE id = "+str(user_id)+"")
    user_info = cursor.fetchall()
    conn.close()
    return user_info