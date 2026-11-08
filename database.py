import sqlite3


def create_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        )
    """)

    conn.commit()
    conn.close()


def add_user(name, age):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Users (name, age) VALUES (?, ?)",
        (name, age)
    )

    conn.commit()
    conn.close()


def update_user(user_id, new_name, new_age):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Users SET name = ?, age = ? WHERE id = ?",
        (new_name, new_age, user_id)
    )

    updated = cursor.rowcount

    conn.commit()
    conn.close()

    return updated


def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Users WHERE id = ?",
        (user_id,)
    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted


create_table()

