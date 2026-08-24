import os
import sqlite3
from datetime import datetime

# Проверяем окружение: на Amvera пишем в постоянный диск, на Mac — локально в проект
if os.path.exists('/data'):
    DB_PATH = '/data/users.db'
else:
    DB_PATH = 'users.db'

def get_connection():
    """Создает безопасное подключение к БД с защитой от блокировок"""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    # WAL-режим защищает базу данных от повреждений и обнуления
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

def init_db():
    """Создает таблицу пользователей с полем даты, если её нет"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            reg_date TEXT DEFAULT (date('now', 'localtime'))
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id: int):
    """Безопасно добавляет ID пользователя при старте бота"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        conn.close()

def get_users_count() -> int:
    """Возвращает общее количество уникальных пользователей за ВСЁ время"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def get_today_users_count() -> int:
    """Возвращает количество НОВЫХ пользователей за сегодня"""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM users WHERE reg_date = ?', (today,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

init_db()

