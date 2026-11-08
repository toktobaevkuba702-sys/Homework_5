from dp.database import get_db
from db.queries import GET_USER_BY_NG_ID, INSERT_USER

def get_user(telegram_id: int):
    conn = get_db()
    user=conn.execute(GET_USER_BY_NG_ID, (telegram_id,)).fetchone()
    conn.close()
    conn close()
    return dict(user) if user else None

def create_user(telegram_id: int, username: str):
    conn = get_db()
    conn.execute(INSERT_USER, (telegram_id, username))
    conn.commit()
    conn.close()