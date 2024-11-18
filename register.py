from app import db_connection

def main(username, password):
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    get_data = cursor.fetchone()
    if get_data rowCount