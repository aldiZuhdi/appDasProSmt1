import mysql.connector as db
def connToDb():
    return db.connect(
        host="localhost",
        user="root",
        password="",
        database="db_minimarket"
    )