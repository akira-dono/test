import sqlite3

db = sqlite3.connect("test.db")
cursor = db.cursor()

table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER UNSIGNED,
    text TEXT
)
"""
# links TEXT

cursor.execute(table)
db.commit()


def insert_user(tg_id):
    sql = """INSERT INTO users (tg_id, text) VALUES (?, "")"""
    cursor.execute(sql, (tg_id, ))
    db.commit()


def get_text(tg_id):
    sql = "SELECT text FROM users WHERE tg_id = ?"
    result = cursor.execute(sql, (tg_id, )).fetchone()[0]
    return result


def update_text(tg_id, text):
    sql = "UPDATE users SET text = ? WHERE tg_id = ?"
    cursor.execute(sql, (text, tg_id))
    db.commit()


def get_user_by_tg_id(tg_id):
    sql = "SELECT * FROM users WHERE tg_id = ?"
    result = cursor.execute(sql, (tg_id, )).fetchone()
    return result


def get_user_ids():
    sql = "SELECT tg_id FROM users"
    result = cursor.execute(sql).fetchall()
    return result
