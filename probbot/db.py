import sqlite3
from datetime import datetime

DB_PATH = 'users.db'

def init_db():
    """Создает таблицу пользователей с полем даты"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Добавляем колонку reg_date, которая по умолчанию хранит текущую дату
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            reg_date TEXT DEFAULT (date('now', 'localtime'))
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id: int):
    """Добавляет ID пользователя и фиксирует дату запуска"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Если пользователь уже есть, INSERT OR IGNORE просто пропустит его, не меняя дату первого старта
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def get_users_count() -> int:
    """Возвращает общее количество уникальных пользователей за ВСЁ время"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_today_users_count() -> int:
    """Возвращает количество НОВЫХ пользователей, запустивших бота СЕГОДНЯ"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Получаем текущую дату в формате YYYY-MM-DD
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM users WHERE reg_date = ?', (today,))
    total = cursor.fetchone()[0]
    conn.close()
    return total
